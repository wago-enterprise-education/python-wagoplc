from fb import Torsteuerung

def porta_westfalica(
        oTorsteuerung_FB: Torsteuerung, xEndlageS1: bool,
        xEndlageS2: bool, xS1: bool, xS2: bool):
    oTorsteuerung_FB(xS1, xS2, xEndlageS1, xEndlageS2)
    print(oTorsteuerung_FB.tor_auf, oTorsteuerung_FB.tor_zu)

    return dict(oTorsteuerung_FB=oTorsteuerung_FB)