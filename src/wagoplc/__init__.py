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

from wagoplc.constants import SCRIPT_PATH
# All usable interfaces
from wagoplc.controller import (
    DI as DI,
    DO as DO,
    AI as AI,
    AO as AO,
    NI as NI,
    PT as PT,
    DIO as DIO,
    AIO as AIO
)
from wagoplc.read_config import read_config
from wagoplc.tasks import Tasks, Scheduler

def main(tasks_object: Tasks | None = None):
    """Main entry point to invoke the scheduler.

    tasks_object: a task registrator given from the main script
    """
    sys.path.append(SCRIPT_PATH)
    tasks, _, plc_obj = read_config(tasks_object)
    scheduler = Scheduler(tasks, plc_obj)
    scheduler.run_tasks()