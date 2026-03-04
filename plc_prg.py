from wagoplc import main, PLC, DI, DO

plc = PLC()

@plc.setup
def setup():
    xEndlageS1 = DI(1)
    xTaster = DI(2)
    xMotor = DO(1)
    xLuefter = DO(2)

    return locals()

@plc.task(
        name = "start the motor",
        cycle_ms = 5
)
def start_motor(xEndlageS1):
    xMotor = True
    if xEndlageS1:
        xMotor = False

    return locals()

def fan(xTaster):
    if xTaster:
        if xLuefter:
            xLuefter = False
        else:
            xLuefter = True

    return locals()

if __name__ == "__main__":
    main()