from wagoplc import main
import time

def ampelschaltung(normalbetrieb, wartungsbetrieb, status, phase_wechsel_zeit, aGelb_zuletzt):
    jetzt = time.time()
    aRot = False
    aGelb = False
    aGruen = False
    bRot = False
    bGelb = 0
    bGruen = 0

    if wartungsbetrieb:
        # Ampel Straße A
        aRot = False
        aGelb = aGelb_zuletzt = not aGelb_zuletzt
        aGruen = False

        # Ampel Straße B
        bRot = False
        bGelb = 10000 if aGelb else 0
        bGruen = 0
    elif normalbetrieb:

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
                aRot = True
                bRot = True

            # 1 — Straße A Rot/Gelb
            case 1:
                aRot = True;  aGelb = True
                bRot = True

            # 2 — Straße A Grün
            case 2:
                aGruen = True
                bRot = True

            # 3 — Straße A Gelb
            case 3:
                aGelb = True
                bRot = True

            # 4 — Straße B Rot/Gelb
            case 4:
                aRot = True
                bRot = True;  bGelb = 10000

            # 5 — Straße B Grün
            case 5:
                aRot = True
                bGruen = 10000

            # 6 — Straße B Gelb
            case 6:
                aRot = True
                bGelb = 10000

    return dict(
        aRot=aRot,aGelb=aGelb,aGruen=aGruen,
        bRot=bRot,bGelb=bGelb,bGruen=bGruen,
        status=status,
        phase_wechsel_zeit=phase_wechsel_zeit,
        aGelb_zuletzt=aGelb_zuletzt
    )

if __name__ == "__main__":
    main()
