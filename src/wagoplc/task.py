import time
import os

from wagoplc.cc100.cc100_9301 import CC100_9301
from wagoplc.cc100.cc100_9401 import CC100_9401
from wagoplc.cc100.cc100_9403 import CC100_9403

TEST_DATA = os.getenv("TESTDATA", os.getcwd() + "/test_data")

def get_controller():
    controller_id = os.getenv("CONTROLLER_ID", "751-9301")
    
    model, version = controller_id.split("-")
    model = int(model)
    version = int(version)

    # print(model)   # 751
    # print(version)  # 9301
    
    if model == 751:
        if version == 9301:
            cc_Obj = CC100_9301()
        elif version == 9401:
            cc_Obj = CC100_9401()
        elif version == 9403:
            cc_Obj = CC100_9403()
        return cc_Obj

class CycleTimeException(Exception): pass

class Task:
    def __init__(self, cycle_func: function = None, cycletime: int = 100, watchdog: int = 400):
        self.cycle_func = cycle_func
        self.cycletime = cycletime
        self.watchdog = watchdog

    def config(self):
        def decorator_config(func):
            ...

    def __call__(self, _func: function = None, *, cycletime: int = 100, watchdog: int = 400):
        """Register task.
        
        cycletime: cycle time in ms, defaults to 100
        watchdog: watchdog time in ms, defaults to 400
        """
        self.cycletime = cycletime
        self.watchdog = watchdog
        def decorator_task(func):
            self.cycle_func = func
            return func
        if _func is None:
            return decorator_task
        return decorator_task(_func)
    
    def loop(self):
        """Run the task in cycles."""
        cc_obj = get_controller()
        # TODO: filter out files that need only be read once
        read_fds = {path: open(TEST_DATA + path.replace(":", "_"), "r") for path in cc_obj.get_read_paths()}
        # Read digital output file initially and add it to the input image.
        # The value is updated after every write, the file is kept open
        # in write mode.  Otherwise, it would be necessary to use update file mode
        # (r+), which is too costly.
        for path in cc_obj.get_read_once_paths():
            with open(TEST_DATA + path, "r") as f:
                cc_obj.input_image[path] = f.read()

        write_fds = {path: open(TEST_DATA + path.replace(":", "_"), "w") for path in cc_obj.get_write_paths()}
        try:
            while True:
                # TODO: Implement cycle time and watchdog
                start = time.time()
                cc_obj.read_inputs(read_fds)
                self.cycle_func(cc_obj)
                cc_obj.write_outputs(write_fds)
                end = time.time()
                duration = (end - start) * 1000
        except Exception as e:
            raise
        finally:
            print("Closing file descriptors...")
            (file.close() for file in read_fds.values())
            (file.close() for file in write_fds.values())