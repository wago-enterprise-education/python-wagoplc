import importlib
import sys

from wagoplc.plc import PLC, DI, DO, AI, AO

def main():
    """
    Main runtime loop to run the given task in cycles.
    """
    #sys.path.append("/home/user/python_bootapplication/")
    plc_prg = importlib.import_module("plc_prg")
    plc = plc_prg.plc
    plc.run_tasks()