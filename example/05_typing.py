# Variant, which uses the library to implement a PLC runtime

from wagoplc import App, DigitalInput, DigitalOutput, AnalogOutput

app = App(...)

def combine_and(i1: bool, i2: bool) -> bool:
    return i1 and i2

@app.task(cycletime=100)
def fb1(di1: DigitalInput(1), di2: DigitalInput(2)) -> DigitalOutput(1):
    # do stuff...
    return combine_and(di1, di2)

@app.task(cycletime=10)
def fb2(di3: DigitalInput(3)) -> (DigitalOutput(2), AnalogOutput(1)):
    return not di3, 42.0

if __name__ == '__main__':
    app.run()

# Could be run with these command:
# plc_prg run -> Starts the PLC runtime, which will execute the loop function in a cycle, reading the inputs and writing the outputs of the PLC.
# plc_prg status -> Shows the current status of the PLC runtime, including the current cycle time and the values of the inputs and outputs.
# plc_prg stop -> Stops the PLC runtime. Terminates the daemon process that is running the PLC runtime. After stopping, the PLC will no longer execute the loop function and will not read or write any inputs or outputs.
