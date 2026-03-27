"""The wagoplc library.

Packages:
- cc100: all functionality specific to the CC100 controller
Modules:
- constants: all top-level constants
- controller: controller superclass and I/O classes
- exceptions: all library exceptions
- fb: standard library function blocks
- read_config: read the configuration file
- tasks: task management for all controllers
"""

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