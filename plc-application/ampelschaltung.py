from wagoplc import main, Tasks, DI, DO, AO
import time

tasks = Tasks()

@tasks.setup
def setup():
    xNormalbetrieb = DI(1)
    xWartungsbetrieb = DI(2)
    aRot = DO(1)
    aGelb = DO(2)
    aGruen = DO(3)
    bRot = DO(4)
    bGelb = AO(1)
    bGruen = AO(2)
    status = 0
    phase_wechsel_zeit = 0
    aGelb_zuletzt = False

    return locals()

@tasks.register(
        name = "Ampelschaltung",
        cycle_ms = 1000
)
def ampelschaltung(xNormalbetrieb, xWartungsbetrieb,status,phase_wechsel_zeit,aGelb_zuletzt):
    jetzt = time.time()
    aRot = False
    aGelb = False
    aGruen = False
    bRot = False
    bGelb = 0
    bGruen = 0

    if xWartungsbetrieb:
        # Ampel Straße A
        aRot = False
        aGelb = aGelb_zuletzt = not aGelb_zuletzt
        aGruen = False

        # Ampel Straße B
        bRot = False
        bGelb = 10000 if aGelb else 0
        bGruen = 0

    if xNormalbetrieb:

        phasen_zeiten = {
            0: 2,   # beide Rot
            1: 2,   # A Rot/Gelb
            2: 6,   # A Gruen
            3: 2,   # A Gelb
            4: 2,   # B Rot/Gelb
            5: 6,   # B Gruen
            6: 2    # B Gelb
        }

        if jetzt - phase_wechsel_zeit >= phasen_zeiten[status]:
            status += 1
            status = 0 if status == 7 else status
            phase_wechsel_zeit = jetzt

        match status:

            # 0 — beide Rot
            case 0:
                aRot = True;  aGelb = False; aGruen = False
                bRot = True;  bGelb = 0;     bGruen = 0

            # 1 — Straße A Rot/Gelb
            case 1:
                aRot = True;  aGelb = True;  aGruen = False
                bRot = True;  bGelb = 0;     bGruen = 0

            # 2 — Straße A Grün
            case 2:
                aRot = False; aGelb = False; aGruen = True
                bRot = True;  bGelb = 0;     bGruen = 0

            # 3 — Straße A Gelb
            case 3:
                aRot = False; aGelb = True;  aGruen = False
                bRot = True;  bGelb = 0;     bGruen = 0

            # 4 — Straße B Rot/Gelb
            case 4:
                aRot = True;  aGelb = False; aGruen = False
                bRot = True;  bGelb = 10000; bGruen = 0

            # 5 — Straße B Grün
            case 5:
                aRot = True;  aGelb = False; aGruen = False
                bRot = False; bGelb = 0;     bGruen = 10000

            # 6 — Straße B Gelb
            case 6:
                aRot = True;  aGelb = False; aGruen = False
                bRot = False; bGelb = 10000; bGruen = 0

    return dict(
        aRot=aRot,aGelb=aGelb,aGruen=aGruen,
        bRot=bRot,bGelb=bGelb,bGruen=bGruen,
        status=status,
        phase_wechsel_zeit=phase_wechsel_zeit,
        aGelb_zuletzt=aGelb_zuletzt
    )

if __name__ == "__main__":
    main(tasks)
