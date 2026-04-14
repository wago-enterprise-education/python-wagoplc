from wagoplc.fb import RS

def light_ctrl(oLicht_An_RS: RS, xTaster: bool, xTaster_Aus: bool, iStatus: int):
    oLicht_An_RS(s=xTaster, r=xTaster_Aus)
    xLicht = oLicht_An_RS.q

    return dict(oLicht_An_RS=oLicht_An_RS, iStatus=iStatus, xLicht=xLicht)