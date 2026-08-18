# Library code

class PLC:
     
     def __init__(self):
          self.tasks = {}
     
     def setup(self):
          """Get user variables."""
          def decorator_setup(func):
               ...
     
     def task(
               self, _func: function = None, *,
               priority: int = 15, watchdog: int = 400000,
               cycletime: int = 50):
          """Register task."""
          def decorator_task(func):
               ...

class Task:
     
     def __init__(self):
          self.cycle_func = None
          self.user_vars = {}
          self.cc_obj = None
     
     def cycle(self):
          """Run one loop cycle."""
          input_image = self.cc_obj.read_inputs(self.user_vars)
          output_image = self.cycle_func(**input_image)
          self.cc_obj.write_outputs(output_image)

# --------------------------------------------------
# plc_prg.py

from wagoplc import main, PLC, DI, DO

plc = PLC()

@plc.setup
def setup():
    xEndlageS1 = DI(1)
    xLuefter = DO(1)

    return locals()

@plc.task(cycletime=5)
def loop(xEndlageS1):
        if xEndlageS1:
            xLuefter = True

        return locals()

if __name__ == "__main__":
    main()