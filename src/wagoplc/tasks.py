from collections.abc import Callable
from typing import Any

import importlib
import inspect
import logging
import signal
import time
import heapq

from wagoplc.controller import DI, DO, AI, AO, IO, IOHandler
from wagoplc.cc100 import CC100_9301, CC100_9401, CC100_9403
from wagoplc.exceptions import NotDefinedError, WatchdogTimeoutError
from wagoplc.read_config import read_config, InvalidConfigError

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="wagoplc.log",
    format="%(levelname)s - %(asctime)s - %(name)s: %(message)s",
    level=logging.DEBUG
)

stop_time = stop_duration = 0
task = None

# Record time when switch is moved to 'stop' via signal handler
def stop_handler(signum, frame):
    logger.debug(f"Caught runtime signal, saving stop time")
    global stop_time
    stop_time = time.time() + 0.0001
    return

# Get stop duration and update running timers before resuming
def cont_handler(signum, frame):
    logger.debug(f"Resuming")
    global stop_time, stop_duration, task
    if task is not None:
          stop_duration = time.time() - stop_time
          print(stop_time)
          task.iohandler.update_timers(stop_duration)
    return
signal.signal(signal.SIGUSR1, stop_handler)
signal.signal(signal.SIGCONT, cont_handler)

class Tasks:
    """Manage task registration per program.
    
    This class collects all variables, the task function and,
    if, given, its configuration. It can be instantiated in the main
    script.
    """

    def __init__(self):
        self.task: dict[str, Any] = None
        # Map of variables and interfaces
        self.map: dict[str, IO] = {}

    def setup(self, func: Callable[[], dict[str, Any]]) -> None:
        """Retrieve variables from function in script.
        
        func: a function that returns all variables as a dict
        """
        def decorator_setup(func):
            logger.debug(f"Reading configuration from script function '{func.__name__}'")
            self.map = func()
            if not isinstance(self.map, dict):
                raise InvalidConfigError("Expected setup function to return a dictionary of variables!")

        return decorator_setup(func)
    
    def register(
            self,
            _func: Callable[..., dict[str, str | int | bool]] = None,
            name: str = "",
            cycle_ms: int = 100,
            watchdog_ms: int = 400000,
            priority: int = 15,
            sensitivity: int = 0):
        """Register a task. Only one is currently allowed.
        
        name:        task name
        cycle_ms:    call cycle time in ms
        priority:    a priority from 1 (highest) to 15
        entry:       task function
        watchdog_ms: maximum runtime in ms before watchdog interrupts
        sensitivity: sensitivity from 0 (highest) to 10
        """
        if self.task:
            raise InvalidConfigError("Only one task per program allowed!")
        def decorator_task(func: Callable[...]):
            self.task = dict(name=name,
                plc_obj=None,
                var_mapping=self.map,
                entry=func,
                cycle_ms=cycle_ms,
                priority=priority,
                watchdog_ms=watchdog_ms,
                sensitivity=sensitivity
            )
            logger.debug(f"Task '{name}' with script entry point '{func.__name__}' registered")
            return func
        
        if _func is None:
            return decorator_task
        return decorator_task(_func)


class Scheduler:
    """A task scheduler."""
    
    def __init__(self, tasks_object: Tasks | None):
        # List of PLC tasks
        self.tasks: list[Task] = []
        # Map of variables
        self.map: dict[str, Any]

        self.tasks_config, config_map, controller_id = read_config()
        if tasks_object is not None:
            config_map.update(tasks_object.map)
        # Catch duplicate I/O mappings
        vars = list(config_map.values())
        duplicate_ios = {
            name: str(value) for name, value in config_map.items()
            if isinstance(value, IO) and vars.count(value) > 1
        }
        if duplicate_ios:
            dups_sorted = dict(sorted(duplicate_ios.items(), key=lambda item: item[1]))
            raise InvalidConfigError(f"Duplicate I/O mappings in configuration: {dups_sorted}")
        self.map = config_map

        self.plc_obj = self._get_controller(controller_id)
        self._read_tasks(tasks_object)

    def _read_tasks(self, tasks_object: Tasks | None = None):
        """Read tasks from configuration and tasks object in script.
        
        tasks_object: task registrator passed from script (default None)
        """
        # Add decorated task
        if tasks_object is not None:
            if task := tasks_object.task:
                task["plc_obj"] = self.plc_obj
                self.tasks.append(Task(**task))

        # Get task definitions from config and retrieve the task function
        for task in self.tasks_config:
            entry: str = task["entry"]
            module_name, func_name = entry.rsplit(".")
            try:
                module = importlib.import_module(module_name)
                task["entry"] = getattr(module, func_name)                
                self.tasks.append(Task(self.plc_obj, self.map, **task))
                logger.debug(f"Task '{task["name"]}' with script entry point '{entry}' registered")
            except ModuleNotFoundError, AttributeError:
                raise NotDefinedError(f"Function '{entry}' for task '{task["name"]}' not defined!")

    def _get_controller(self, controller_id: str):
        """Get controller object by item number.
        
        controller_id: item number
        """
        model, version = controller_id.split("-")
        model = int(model)
        version = int(version)
        
        if model == 751:
            if version == 9301:
                plc_obj = CC100_9301()
            elif version == 9401:
                plc_obj = CC100_9401()
            elif version == 9403:
                plc_obj = CC100_9403()
            plc_obj.init_fds()

        logger.info(f"Using controller with item number '{controller_id}'")
        return plc_obj

    def run_tasks(self):
        """Scheduler to run all tasks in cycles."""
        global stop_time, stop_duration, task
        try:
            if not self.tasks:
                return
            logger.info(f"Found tasks {", ".join(t.name for t in self.tasks)}")

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
                    task.cycle()
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
        except Exception as e:
            raise
        finally:
            self.plc_obj.reset()


class Task:
    """Represent a PLC task."""

    def __init__(
        self,
        plc_obj,
        var_mapping: dict[str, Any],
        name: str,
        entry: Callable[..., dict[str, str | int | bool]],
        cycle_ms: int = 100,
        priority: int = 15,
        watchdog_ms: int = 400000,      
        sensitivity: int = 0):
        """
        name:        task name
        entry:       task function
        cycle_ms:    call cycle time in ms
        priority:    a priority from 1 (highest) to 15
        watchdog_ms: maximum runtime in ms before watchdog interrupts
        sensitivity: sensitivity from 0 (highest) to 10
        """
        self.name = name or "<unnamed task>"
        self.cycle_time = cycle_ms
        self.cycle_func = entry
        self.plc_obj = plc_obj
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

        self.iohandler = IOHandler(
            plc_obj, self._get_input_vars(var_mapping), var_mapping
        )

        self.next_run: float = time.time()
    
    def __lt__(self, other: Task) -> bool:
        return self.priority < other.priority

    def __str__(self):
        return f"Task(name={self.name}, entry={self.cycle_func}, cycle_ms={self.cycle_ms}, priority={self.priority}, watchdog_ms={self.watchdog_ms}, sensitivity={self.sensitivity})"

    def _get_input_vars(self, var_mapping: dict[str, Any]) -> dict[str, Any]:
        """Compare defined variables and parameters and return input mapping.
        
        Raise NotDefinedError if a parameter is not defined as a variable.

        var_mapping: map of user-defined variables 
        """
        func_params = [param.name for param in inspect.signature(self.cycle_func).parameters.values()]
        vars = var_mapping.keys()
        if not_defined := list(filter(lambda p: p not in vars, func_params)):
            raise NotDefinedError(f"Undefined variables: {", ".join(not_defined)}")
        def is_input(pair):
            k, _ = pair
            if k in func_params:
                return True
            return False
        return dict(filter(is_input, var_mapping.items()))

    def cycle(self):
        """Run one task cycle."""
        # Get input image (variables mapped to values)
        input_image = self.iohandler.get_input_image()
        # Get output image (variables mapped to values)
        output_image = self.cycle_func(**input_image)
        if not isinstance(output_image, dict):
            raise NotDefinedError(f"Cycle function '{self.cycle_func.__name__}' did not return an output image!")
        # Actually write outputs, return state variables
        self.iohandler.process_output_image(output_image)

