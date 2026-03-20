import sys

from wagoplc.controller import DI, DO, AI, AO
from wagoplc.tasks import Tasks, Scheduler
from wagoplc.constants import SCRIPT_PATH

def main(tasks_object: Tasks | None = None):
    """
    Main runtime loop to run the given tasks in cycles.
    """
    sys.path.append(SCRIPT_PATH)
    scheduler = Scheduler(tasks_object)
    scheduler.run_tasks()