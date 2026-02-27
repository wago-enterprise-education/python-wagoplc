# plc_prg.py

from wagoplc import main, PLC

plc = PLC()

@plc.task(cycletime=5)
def loop(xEndlageS1):
    if xEndlageS1:
        xLuefter = True

    return xLuefter