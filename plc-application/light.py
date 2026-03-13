from wagoplc.fb import RS

def light_ctrl(oLicht_An_RS: RS, xTaster: bool, xTaster_Aus: bool):
    oLicht_An_RS(s=xTaster, r=xTaster_Aus)
    if oLicht_An_RS.q:
        print("Licht an!")
    else:
        print("Licht aus!")

    return dict(oLicht_An_RS=oLicht_An_RS)