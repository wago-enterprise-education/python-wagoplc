from wagoplc import main, PLC, DI, DO

plc = PLC()

@plc.setup
def setup():
    xEndlageS1 = DI(1)
    xEndlageS2 = DI(2)
    xMotor = DO(1)

    return locals()

@plc.task(cycle_time=5)
def loop(xEndlageS1):
        xMotor = True
        if xEndlageS1:
            xMotor = False

        return locals()

if __name__ == "__main__":
    main()