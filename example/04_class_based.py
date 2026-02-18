# This is part of the wagoplc library:

class Task:
    def __init__(self) -> None:
        super().__init__()
    
    def loop(self) -> None:
        self.read_inputs()
        self.__call__() # Calls into the subclass
        self.write_outputs()

    def __call__(self, *args, **kwargs):
        ...

# This is an example of a class-based PLC program. The main function will call the setup and loop methods of the MyPLC class.

from wagoplc import Task, main, config

@config(
    cycletime=100,
    controller = '0751-9301',
    inputs = ['di1', 'di2'],
    outputs = ['do1', 'ao1']
)
class MyPLC_PRG(Task):
    def __init__(self):
        # This method will be called once when the PLC runtime starts. Use it to initialize any variables or state.
        super().__init__()

    def __call__(self, *args, **kwargs):
        # This method will be called in a cycle by the PLC runtime. 
        # The inputs are read automatically just before the call and the outputs are written automatically just after the call. 
        # Use it to process the logic
        di1 = self.di1
        di2 = self.di2
        self.do1 = di1 and di2
        self.ao1 = 42.0

if __name__ == '__main__':
    main()
