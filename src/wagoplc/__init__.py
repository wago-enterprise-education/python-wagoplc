import importlib
import sys

from wagoplc.plc import PLC, DI, DO, AI, AO
from wagoplc.cc100.constants import PLC_SCRIPT

def main():
    """
    Main runtime loop to run the given tasks in cycles.
    """
    #sys.path.append("/home/user/python_bootapplication/")
    plc_prg = importlib.import_module(PLC_SCRIPT)
    plc = plc_prg.plc
    plc.configure()
    task = plc.tasks[0]
    plc.run_tasks()