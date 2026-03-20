from wagoplc import main, Tasks, DI, DO
from wagoplc.fb import CTUD

tasks = Tasks()

@tasks.setup
def setup():
    xLichtSchrankeRein = DI(1)
    xLichtSchrankeRaus = DI(2)
    xMotor = DO(1)
    oFlasche_Puffer_CTUD = CTUD(pv=3)

    return dict(
        xLichtSchrankeRein=xLichtSchrankeRein,
        xLichtSchrankeRaus=xLichtSchrankeRaus,
        xMotor=xMotor,
        oFlasche_Puffer_CTUD=oFlasche_Puffer_CTUD
    )

@tasks.register(
        name = "bottle filling plant",
        cycle_ms = 5
)
def bottle_filler(xLichtSchrankeRein, xLichtSchrankeRaus, oFlasche_Puffer_CTUD: CTUD):
    oFlasche_Puffer_CTUD(cu=xLichtSchrankeRein, cd=xLichtSchrankeRaus)
    xMotor = True
    print(oFlasche_Puffer_CTUD.cv)
    if oFlasche_Puffer_CTUD.qu:
        print("Motor... aus!")
        xMotor = False

    return dict(xMotor=xMotor, oFlasche_Puffer_CTUD=oFlasche_Puffer_CTUD)

if __name__ == "__main__":
    main(tasks)