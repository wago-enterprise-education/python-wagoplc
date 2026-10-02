from wagoplc import main, Task, DI, AO
from wagoplc.fb import CTUD

xLichtSchrankeRein = DI(1)
xLichtSchrankeRaus = DI(2)
xMotor = AO(1)
oFlasche_Puffer_CTUD = CTUD(pv=3)

def bottle_filler(xLichtSchrankeRein, xLichtSchrankeRaus, oFlasche_Puffer_CTUD: CTUD):
    oFlasche_Puffer_CTUD(cu=xLichtSchrankeRein, cd=xLichtSchrankeRaus)
    # set to 5 V (5000 mV)
    xMotor = 5000
    print(oFlasche_Puffer_CTUD.cv)
    if oFlasche_Puffer_CTUD.qu:
        print("Motor... aus!")
        xMotor = 0

    return dict(xMotor=xMotor, oFlasche_Puffer_CTUD=oFlasche_Puffer_CTUD)

if __name__ == "__main__":
    main(
        Task(name="bottle filling plant", cycle_ms=5, entry=bottle_filler),
        **locals()
    )