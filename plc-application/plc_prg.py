from wagoplc import main, Tasks, DI, DO

tasks = Tasks()

@tasks.setup
def setup():
    xEndlageS1 = DI(1)
    xMotor = DO(1)

    return locals()

@tasks.register(
        name = "start the motor",
        cycle_ms = 5
)
def start_motor(xEndlageS1):
    xMotor = True
    if xEndlageS1:
        xMotor = False

    return locals()

if __name__ == "__main__":
    main(tasks)