# This is an example of a class-based PLC program. The main function will call the setup and loop methods of the MyPLC class.

from wagoplc import PLC_PRG

class MyPLC_PRG(PLC_PRG):
    def setup(self):
        # This method will be called once when the PLC runtime starts. Use it to initialize any variables or state.
        ...

    def loop(self):
        # This method will be called in a cycle by the PLC runtime. Use it to read the inputs, process the logic, and write the outputs.

        di1 = self.digitalread(1)
        di2 = self.digitalread(2)
        do1 = di1 and di2
        self.digitalwrite(1, do1)

if __name__ == '__main__':
    MyPLC_PRG.run()
