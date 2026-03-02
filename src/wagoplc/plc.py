import inspect
import os

from wagoplc.cc100.cc100_v1 import DI, DO, AI, AO
from wagoplc.cc100.cc100_9301 import CC100_9301
from wagoplc.cc100.cc100_9401 import CC100_9401
from wagoplc.cc100.cc100_9403 import CC100_9403

TEST_DATA = os.getenv("TESTDATA", os.getcwd() + "/test_data")

class WAGOPlcError(Exception): pass
class NotDefinedError(Exception): pass

def get_controller():
    controller_id = os.getenv("CONTROLLER_ID", "751-9301")
    
    model, version = controller_id.split("-")
    model = int(model)
    version = int(version)

    # print(model)   # 751
    # print(version)  # 9301
    
    if model == 751:
        if version == 9301:
            cc_obj = CC100_9301()
        elif version == 9401:
            cc_obj = CC100_9401()
        elif version == 9403:
            cc_obj = CC100_9403()
        return cc_obj

class PLC:
    
    def __init__(self):
        self.tasks = []
        self.io_mapping = {}
        self.cc_obj = get_controller()

    def setup(self, func):
        def decorator_setup(func):
            self.io_mapping = func()
        return decorator_setup(func)
    
    def task(self, _func: function = None, *, cycle_time: int = 100, watchdog_time: int = 400):
        """Register task.
        
        cycle_time: cycle time in ms, defaults to 100
        watchdog: watchdog time in ms, defaults to 400
        """
        def decorator_task(func):
            self.tasks.append(
                Task(
                    self.cc_obj,
                    io_mapping=self.io_mapping,
                    cycle_func=func,
                    cycle_time=cycle_time,
                    watchdog_time=watchdog_time
                )
            )
            return func
        if _func is None:
            return decorator_task
        return decorator_task(_func)
            
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

        # TODO: Integrate cycle time and watchdog implementation
        while True:
            try:
                # Run task cycle
                self.tasks[0].cycle()
            except Exception as e:
                raise
            finally:
                print("Closing file descriptors...")
                (file.close() for file in read_fds.values())
                (file.close() for file in write_fds.values())


class Task:

    def __init__(self, cc_obj, io_mapping: dict[str, str], cycle_func: function = None,
                 cycle_time: int = 100, watchdog_time: int = 400):
        self.cc_obj = cc_obj
        self.cycle_func = cycle_func
        self.cycle_time = cycle_time
        self.watchdog_time = watchdog_time
        self.io_mapping = self._filter_params(io_mapping)

    def _filter_params(self):
        """Compare defined and actual parameters and update mapping.
        
        Raise NotDefinedError if a parameter is not defined as a variable. 
        """
        func_params = [param.name for param in inspect.signature(self.cycle_func).parameters.values()]
        vars = self.io_mapping.keys()
        if not_defined := list(filter(lambda p: p not in vars, func_params)):
            raise NotDefinedError(f"Undefined variables: {", ".join(not_defined)}")
        def filter_used(pair):
            k, _ = pair
            if k in func_params:
                return True
            return False
        return dict(filter(filter_used, self.io_mapping.items()))

    def cycle(self, read_fds, write_fds):
        """Run one task cycle."""
        # Get input image (variables mapped to values)
        input_image = self.cc_obj.read_inputs(read_fds, self.io_mapping)
        # Get output image (variables mapped to values)
        output_image = self.cycle_func(**input_image)
        # Actually write outputs
        self.cc_obj.write_outputs(write_fds, output_image)