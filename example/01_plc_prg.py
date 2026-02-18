# Variant, which uses the library to implement a PLC runtime

from wagoplc import App, ProcessImageInput, ProcessImageOutput

app = App()

@app.prg(...)
def loop(pii: ProcessImageInput):
    # do stuff...
    do1 = pii.di1 and pii.di2

    # Return the process image output, which will be written to the outputs of the PLC
    piq = ProcessImageOutput(
        do1=do1,
        do2=False,
        ...
    )
    return piq

if __name__ == '__main__':
    app.run()

# Could be run with these command:
# plc_prg run -> Starts the PLC runtime, which will execute the loop function in a cycle, reading the inputs and writing the outputs of the PLC.
# plc_prg status -> Shows the current status of the PLC runtime, including the current cycle time and the values of the inputs and outputs.
# plc_prg stop -> Stops the PLC runtime. Terminates the daemon process that is running the PLC runtime. After stopping, the PLC will no longer execute the loop function and will not read or write any inputs or outputs.
