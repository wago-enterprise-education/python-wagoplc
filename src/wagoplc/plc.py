from collections.abc import Callable

import importlib
import inspect
import logging
import os
import time
import heapq

from wagoplc.cc100.cc100_v1 import DI, DO, AI, AO, IO
from wagoplc.cc100.cc100_9301 import CC100_9301
from wagoplc.cc100.cc100_9401 import CC100_9401
from wagoplc.cc100.cc100_9403 import CC100_9403
from wagoplc.cc100.constants import PLC_SCRIPT
from wagoplc.read_config import read_config, InvalidConfig

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="wagoplc.log",
    format="%(levelname)s - %(asctime)s - %(name)s: %(message)s",
    level=logging.DEBUG
)

TEST_DATA = os.getenv("TESTDATA", os.getcwd() + "/test_data")

class WAGOPlcError(Exception):
    """Base class for WAGO PLC related errors."""
    pass

class NotDefinedError(WAGOPlcError):
    """Raised when a variable in a task function is not defined in IO mapping."""
    pass

class WatchdogTimeout(WAGOPlcError):
    """Throw when task cycle exceeds maximum allowed time."""
    pass


class Tasks:
    """Manage task registration.
    
    This class collects all variables, the task function and,
    if, given, its configuration. It should be instantiated in every
    program.
    """

    def __init__(self):
        self.task: Task = None
        # Map of variables and interfaces
        self.map: dict[str, IO] = {}
        # Functions of tasks defined in the configuration file
        # Entry point names are mapped to functions
        self.task_func: dict[str, Callable[..., dict[str, str | int | bool]]] = {}

    def setup(self, func: Callable[[], dict[str, IO]]) -> None:
        """Retrieve variables from function in script.
        
        func: a function that returns all variables as a dict
        """
        def decorator_setup(func):
            logger.debug(f"Reading configuration from script function '{func.__name__}'")
            self.map = func()
            if not isinstance(self.map, dict):
                raise InvalidConfig("Expected setup function to return a dictionary of variables!")

        return decorator_setup(func)
    
    def register(
            self,
            _func: Callable[..., dict[str, str | int | bool]] = None,
            name: str = "",
            cycle_ms: int = 100,
            watchdog_ms: int = 400000,
            priority: int = 15,
            sensitivity: int = 0):
        """Register task.
        
        name:        task name
        cycle_ms:    call cycle time in ms
        priority:    a priority from 1 (highest) to 15
        entry:       task function
        watchdog_ms: maximum runtime in ms before watchdog interrupts
        sensitivity: sensitivity from 0 (highest) to 10
        """
        if self.task or self.task_func:
            raise InvalidConfig("Only one task per program allowed!")
        def decorator_task(func: Callable[...]):
            self.task = Task(
                name=name,
                cc_obj=None,
                io_mapping=self.map,
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
        
        # Task is (likely) defined in the config file
        # save it for later
        self.task_func[_func.__name__] = _func
        return _func


class PLC:
    """Represent a programmable logic controller (PLC)."""
    
    def __init__(self, tasks_object: Tasks):
        # List of PLC tasks
        self.tasks: list[Task] = []
        # Map of variables and interfaces
        self.map: dict[str, IO] = tasks_object.map

        self.tasks_config, config_map, controller_id = read_config()
        config_map.update(self.map)
        # Catch duplicate mappings
        ios = list(config_map.values())
        duplicates = {name: str(io) for name, io in config_map.items() if ios.count(io) > 1}
        if duplicates:
            dups_sorted = dict(sorted(duplicates.items(), key=lambda item: item[1]))
            raise InvalidConfig(f"Duplicate I/O mappings in configuration: {dups_sorted}")
        self.map = config_map
        self.cc_obj = self._get_controller(controller_id)
        self._read_tasks(tasks_object)

    def _read_tasks(self, tasks_object: Tasks):
        """Read tasks from configuration and tasks object in script.
        
        tasks_object: task registrator passed from script
        """
        # Add decorated task
        if task := tasks_object.task:
            task.cc_obj = self.cc_obj
            self.tasks.append(task)

        # Get task definition from config
        for task in self.tasks_config:
            entry: str = task["entry"]
            module_name, func_name = entry.rsplit(".")
            try:
                if module_name == PLC_SCRIPT:
                    # Function defined in main script
                    task["entry"] = tasks_object.task_func[func_name]
                else:
                    # Try to import
                    module = importlib.import_module(module_name)
                    task["entry"] = module.tasks.task_func[func_name]
                
                self.tasks.append(Task(self.cc_obj, self.map, **task))
                logger.debug(f"Task '{task["name"]}' with script entry point '{entry}' registered")

            except KeyError, ModuleNotFoundError:
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
                cc_obj = CC100_9301()
            elif version == 9401:
                cc_obj = CC100_9401()
            elif version == 9403:
                cc_obj = CC100_9403()
            logger.info(f"Using controller with item number '{controller_id}'")
            return cc_obj

    def run_tasks(self):
        """Scheduler to run all tasks in cycles."""
        read_fds = {path: open(TEST_DATA + path.replace(":", "_"), "r") for path in self.cc_obj.get_read_paths()}
        # Read digital output file initially and add it to the input image.
        # The value is updated after every write, the file is kept open
        # in write mode.  Otherwise, it would be necessary to use update file mode
        # (r+), which is too costly.
        for path in self.cc_obj.get_read_once_paths():
            with open(TEST_DATA + path, "r") as f:
                self.cc_obj.input_image[path] = f.read()

        write_fds = {path: open(TEST_DATA + path.replace(":", "_"), "w") for path in self.cc_obj.get_write_paths()}

        try:
            if not self.tasks:
                return
            logging.info(f"Found tasks {", ".join(t.name for t in self.tasks)}")

            now = time.time()
            for t in self.tasks:
                t.next_run = now

            logger.info("Starting tasks execution")
            while True:
                now = time.time()
                ready = []

                for t in self.tasks:
                    if now >= t.next_run:
                        heapq.heappush(ready, t)

                while ready:
                    task = heapq.heappop(ready)
                    print(f"Running task {task.name} with priority {task.priority} (every {task.cycle_ms} ms)")

                    start_perf = time.perf_counter()
                    # Run task cycle
                    task.cycle(read_fds, write_fds)
                    duration_ms = (time.perf_counter() - start_perf) * 1000.0

                    if duration_ms > task.watchdog_ms:
                        raise WatchdogTimeout(
                            f"Task '{task.name}' has been caught by the watchdog: "
                            f"{duration_ms:.3f} ms > {task.watchdog_ms:.3f} ms"
                        )

                    task.next_run += task._cycle_s

                time.sleep(0.0005)
        except Exception as e:
            raise
        finally:
            logger.info("Resetting outputs...")
            self.cc_obj.reset_outputs(write_fds)
            logger.debug("Closing file descriptors...")
            (file.close() for file in read_fds.values())
            (file.close() for file in write_fds.values())


class Task:
    """Represent a PLC task."""

    def __init__(
        self,
        cc_obj,
        io_mapping: dict[str, IO],
        name: str,
        cycle_ms: int = 100,
        priority: int = 15,
        entry: Callable[..., dict[str, str | int | bool]] = None,
        watchdog_ms: int = 400000,      
        sensitivity: int = 0):
        """
        name:        task name
        cycle_ms:    call cycle time in ms
        priority:    a priority from 1 (highest) to 15
        function:    task function
        watchdog_ms: maximum runtime in ms before watchdog interrupts
        sensitivity: sensitivity from 0 (highest) to 10
        """
        self.name = name
        self.cycle_time = cycle_ms
        self.cycle_func = entry
        self.cc_obj = cc_obj
        if cycle_ms < 1:
            cycle_ms = 1
        elif cycle_ms > 10000:
            cycle_ms = 10000
        self.cycle_ms = cycle_ms
        self._cycle_s = cycle_ms / 1000.0

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

        self.inputs = self._get_inputs(io_mapping)
        self.outputs = self._get_outputs(io_mapping)

        self.next_run: float = time.time()
    
    def __lt__(self, other: Task) -> bool:
        return self.priority < other.priority

    def _get_inputs(self, io_mapping: dict[str, IO]) -> dict[str, AO | DO]:
        """Compare defined and actual parameters and return input mapping.
        
        Raise NotDefinedError if a parameter is not defined as a variable.

        io_mapping: map of user-defined variables 
        """
        func_params = [param.name for param in inspect.signature(self.cycle_func).parameters.values()]
        vars = io_mapping.keys()
        if not_defined := list(filter(lambda p: p not in vars, func_params)):
            raise NotDefinedError(f"Undefined variables: {", ".join(not_defined)}")
        def is_input(pair):
            k, v = pair
            if not isinstance(v, IO):
                raise ValueError("Variables must be mapped to I/O objects!")
            if k in func_params:
                return True
            return False
        return dict(filter(is_input, io_mapping.items()))
    
    def _get_outputs(self, io_mapping: dict[str, any])-> dict[str, any]:
        """Get output variables from mapping.
        
        io_mapping: map of user-defined variables
        """
        return dict(
            filter(
                lambda map: isinstance(map[1], (DO, AO)), 
                io_mapping.items()
            )
        )

    def cycle(self, read_fds: dict[str, any], write_fds: dict[str, any]) -> None:
        """Run one task cycle."""
        # Get input image (variables mapped to values)
        input_image = self.cc_obj.read_inputs(read_fds, self.inputs)
        # Get output image (variables mapped to values)
        output_image = self.cycle_func(**input_image)
        if not isinstance(output_image, dict):
            raise NotDefinedError(f"Cycle function '{self.cycle_func.__name__}' did not return an output image!")
        # Actually write outputs
        self.cc_obj.write_outputs(write_fds, output_image, self.outputs)
