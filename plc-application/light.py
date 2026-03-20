from wagoplc.fb import RS

def light_ctrl(oLicht_An_RS: RS, xTaster: bool, xTaster_Aus: bool, iStatus: int):
    oLicht_An_RS(s=xTaster, r=xTaster_Aus)
    match iStatus:
        case 0:
            if oLicht_An_RS.q:
                print("Licht an!")
                iStatus = 1
        case 1:
            if not oLicht_An_RS.q:
                print("Licht aus!")
                iStatus = 0

    return dict(oLicht_An_RS=oLicht_An_RS, iStatus=iStatus)