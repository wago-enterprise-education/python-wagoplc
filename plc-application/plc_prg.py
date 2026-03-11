from wagoplc import main, Tasks, DI, DO
from wagoplc.fb import CTU

tasks = Tasks()

@tasks.setup
def setup():
    xEndlageS1 = DI(1)
    xMotor = DO(1)
    oMotor_Drehzahl_CTU = CTU(pv=3)

    return dict(
        xEndlageS1=xEndlageS1,
        xMotor=xMotor,
        oMotor_Drehzahl_CTU=oMotor_Drehzahl_CTU
    )

@tasks.register(
        name = "start the motor",
        cycle_ms = 5
)
def start_motor(xEndlageS1, oMotor_Drehzahl_CTU: CTU):
    oMotor_Drehzahl_CTU(cu=xEndlageS1)
    xMotor = True
    print(oMotor_Drehzahl_CTU.cv, oMotor_Drehzahl_CTU.q)
    if oMotor_Drehzahl_CTU.q:
        xMotor = False

    return dict(xMotor=xMotor, oMotor_Drehzahl_CTU=oMotor_Drehzahl_CTU)

if __name__ == "__main__":
    main(tasks)