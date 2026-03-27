from wagoplc.fb import TON, TOF

def fan(xTaster, oLuefter_Einschalt_TON: TON, 
        iStatus: int, xLuefterAn: bool, xLuefterAus: bool,
        oLuefter_Ausschalt_TOF: TOF):
    oLuefter_Einschalt_TON(start=xLuefterAn, pt=10)
    oLuefter_Ausschalt_TOF(start=xLuefterAus, pt=15)

    print(iStatus)

    match iStatus:
        case 0: # Luefter ist aus
            xLuefter = False
            if xTaster:
                print("Starte Luefter!")
                xLuefterAn = True
                iStatus = 1
        case 1: # Warten...
            xLuefter = False
            print(oLuefter_Einschalt_TON.et)
            if oLuefter_Einschalt_TON.q:
                print("Es werde Luft!")
                xLuefter = True
                xLuefterAn = False
                iStatus = 2
        case 2: # Luefter laeuft
            xLuefter = True
            xLuefterAn = False
            print("Und er läuft!")
            if xTaster:
                xLuefterAus = True
                iStatus = 3
        case 3: # Luefter faehrt herunter
            xLuefter = oLuefter_Ausschalt_TOF.q
            print(oLuefter_Ausschalt_TOF.et)
            if not xLuefter:
                print("Aus!")
                xLuefterAus = False
                iStatus = 0
    
    return dict(oLuefter_Einschalt_TON=oLuefter_Einschalt_TON, iStatus=iStatus,
                xLuefter=xLuefter, xLuefterAn=xLuefterAn, oLuefter_Ausschalt_TOF=oLuefter_Ausschalt_TOF, xLuefterAus=xLuefterAus)
