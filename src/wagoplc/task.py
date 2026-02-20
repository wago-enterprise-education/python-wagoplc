import dataclasses
import time

from wagoplc.cc100.cc100_9301 import CC100_9301, SYSTEM_PATHS

TEST_DATA = "C:/Users/U0130807/repos/python-wagoplc/test_data"

class CycleTimeException(Exception): pass

class Task:
    def __init__(self, cycle_func: function = None, cycletime: int = 100):
        self.cycle_func = cycle_func
        self.cycletime = cycletime

    def config(self, func):
        ...

    def __call__(self, _func: function = None, *, cycletime: int = 100):
        """Register task.
        
        cycletime: time in ms, defaults to 100
        """
        self.cycletime = cycletime
        def decorator_task(func):
            self.cycle_func = func
            return func
        if _func is None:
            return decorator_task
        return decorator_task(_func)
    
    def loop(self):
        """Run the task in cycles."""
        paths = SYSTEM_PATHS()
        # TODO: filter out files that need only be read once
        read_fds = {path: open(TEST_DATA + path.replace(":", "_"), "r") for path in paths.get_read_paths()}
        cc_obj = CC100_9301()
        # Read digital output file initially and add it to the input image.
        # The value is updated after every write, the file is kept open
        # in write mode.  Otherwise, it would be necessary to use update file mode
        # (r+), which is too costly.
        with open(TEST_DATA + paths.DOUT_DATA, "r") as f:
            cc_obj.input_image[paths.DOUT_DATA] = f.read()

        write_fds = {path: open(TEST_DATA + path.replace(":", "_"), "w") for path in paths.get_write_paths()}
        try:
            while True:
                start = time.time()
                cc_obj.read_inputs(read_fds)
                self.cycle_func(cc_obj)
                cc_obj.write_outputs(write_fds)
                end = time.time()
                duration = (end - start) * 1000
                if duration <= self.cycletime:
                    time.sleep((self.cycletime - duration) / 1000)
                else:
                    raise CycleTimeException("This took too long!!")
        except Exception as e:
            raise
        finally:
            print("Closing file descriptors...")
            (file.close() for file in read_fds.values())
            (file.close() for file in write_fds.values())