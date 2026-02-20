import importlib
import sys

from wagoplc.task import Task

def main():
    """
    Main runtime loop to run the given task in cycles.
    """
    sys.path.append("/home/kilian/wago_plc/")
    plc_prg = importlib.import_module("plc_prg")
    task = plc_prg.task
    task.loop()