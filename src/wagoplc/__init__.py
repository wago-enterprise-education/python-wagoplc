import sys

from wagoplc.plc import Tasks, PLC, DI, DO, AI, AO
from wagoplc.constants import SCRIPT_PATH

def main(tasks_object: Tasks | None = None):
    """
    Main runtime loop to run the given tasks in cycles.
    """
    sys.path.append(SCRIPT_PATH)
    plc = PLC(tasks_object)
    task = plc.tasks[0]
    plc.run_tasks()