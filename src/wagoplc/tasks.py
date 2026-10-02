"""Task management.

This module holds the classes responsible for task management.
- Task: a single task
- Scheduler: task scheduler
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import logging
import signal
import time
import heapq

from wagoplc.constants import LOG_FILE
from wagoplc.controller import IO, IOHandler, Controller
from wagoplc.exceptions import NotDefinedError, WatchdogTimeoutError

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=LOG_FILE,
    format="%(levelname)s - %(asctime)s - %(name)s: %(message)s",
    level=logging.DEBUG
)

stop_time = stop_duration = 0
task = None
# Record time when switch is moved to 'stop' via signal handler
def stop_handler(signum, frame):
        logger.debug("Caught runtime signal, saving stop time")
        global stop_time
        stop_time = time.time() + 0.0001
        return

# Get stop duration and update running timers before resuming
def cont_handler(signum, frame):
        logger.debug("Resuming")
        global stop_time, stop_duration, task
        if task is not None:
            stop_duration = time.time() - stop_time
            task.iohandler.update_timers(stop_duration)
        return
signal.signal(signal.SIGUSR1, stop_handler)
signal.signal(signal.SIGCONT, cont_handler)


class Task:
    """Represent a PLC task."""

    def __init__(
        self,
        name: str,
        entry: Callable[..., dict[str, str | int | bool]],
        cycle_ms: int = 100,
        priority: int = 15,
        watchdog_ms: int = 400000,      
        sensitivity: int = 0):
        """Configure the task.

        Raise ValueError if priority or sensitivity are not within the
        allowed ranges. Raise NotDefinedError via _get_input_vars if
        there are undefined variables in the input parameters.

        name:        task name
        entry:       task function
        cycle_ms:    call cycle time in ms
        priority:    a priority from 1 (highest) to 15
        watchdog_ms: maximum runtime in ms before watchdog interrupts
        sensitivity: sensitivity from 0 (highest) to 10
        """
        self.name = name or "<unnamed task>"
        self.cycle_func = entry
        if cycle_ms < 1:
            cycle_ms = 1
        elif cycle_ms > 10000:
            cycle_ms = 10000
        self.cycle_ms = cycle_ms

        if priority not in range(1, 16):
            raise ValueError("priority must be between 1 and 15.")
        self.priority = priority

        if watchdog_ms < 0:
            watchdog_ms = 0
        elif watchdog_ms > 400000:
            watchdog_ms = 400000

        if sensitivity not in range(0, 11):
            raise ValueError("sensitivity must be between 0 and 10.")
        self.sensitivity = sensitivity

        self.watchdog_ms = watchdog_ms * (self.sensitivity * 0.05 + 1.0)

        self.inputs: dict[str, IO] = {}
        self.state_vars: dict[str, Any]

        self.next_run: float = time.time()
    
    def __lt__(self, other: "Task") -> bool:
            return self.priority < other.priority

    def __str__(self) -> str:
            return f"Task(name={self.name}, entry={self.cycle_func}, cycle_ms={self.cycle_ms}, priority={self.priority}, watchdog_ms={self.watchdog_ms}, sensitivity={self.sensitivity})"


class Scheduler:
    """A task scheduler.
    
    - run_tasks: run the collected tasks
    """
    
    def __init__(self, tasks: list[Task], iohandler: IOHandler, plc_obj: Controller) -> None:
        """Configure the scheduler.

        :param tasks: List of Task objects to run
        :param plc_obj: The controller object
        :param var_mapping: The complete variable mapping
        """
        self.tasks = tasks
        self.plc_obj = plc_obj
        self.iohandler = iohandler

    def run_tasks(self):
        """Scheduler to run all tasks in cycles."""
        global stop_time, stop_duration, task
        try:
            if not self.tasks:
                return
            logger.info(f"Found tasks {', '.join(t.name for t in self.tasks)}")

            now = time.time()
            for t in self.tasks:
                t.next_run = now

            logger.info("Starting tasks execution")
            while True:
                now = time.time()
                ready: list[Task] = []

                for t in self.tasks:
                    if now >= t.next_run:
                        heapq.heappush(ready, t)
                while ready:
                    task = heapq.heappop(ready)
                    print(f"Running task {task.name} with priority {task.priority} at {task.next_run} (every {task.cycle_ms} ms)")

                    start_perf = time.perf_counter()

                    # Run task cycle
                    # Get input image (variables mapped to values)
                    input_image = self.iohandler.get_input_image(task)
                    # Get output image (variables mapped to values)
                    output_image = task.cycle_func(**input_image)
                    if not isinstance(output_image, dict):
                        raise NotDefinedError(f"Cycle function '{task.cycle_func.__name__}' did not return an output image!")
                    # Actually write outputs, return state variables
                    self.iohandler.process_output_image(task, output_image)

                    duration_ms = (time.perf_counter() - start_perf - stop_duration) * 1000.0
                    stop_duration = 0
                    if duration_ms > task.watchdog_ms:
                        raise WatchdogTimeoutError(
                            f"Task '{task.name}' has been caught by the watchdog: "
                            f"{duration_ms:.3f} ms > {task.watchdog_ms:.3f} ms"
                        )
                    # Next run is scheduled after cycle time passes
                    task.next_run = time.time() + (task.cycle_ms / 1000.0)

                time.sleep(0.0005)
        except Exception:
            raise
        finally:
            self.plc_obj.reset()

