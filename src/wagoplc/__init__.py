from wagoplc.plc import Tasks, PLC, DI, DO, AI, AO
from wagoplc.cc100.constants import PLC_SCRIPT, SCRIPT_PATH

def main(tasks_object: Tasks):
    """
    Main runtime loop to run the given tasks in cycles.
    """
    plc = PLC(tasks_object)
    task = plc.tasks[0]
    plc.run_tasks()