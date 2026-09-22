"""
The wagoplc library.
"""

from __future__ import annotations

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
import wagoplc.read_config as read_config
from wagoplc.tasks import Task, Scheduler

def main(task: Task | None = None, **script_vars):
    """Main entry point to invoke the scheduler.

    tasks: a task given from the main script
    vars: variables given from the script as keyword arguments
    """
    sys.path.append(SCRIPT_PATH)
    tasks, iohandler, plc_obj = read_config.read_config(task, **script_vars)
    scheduler = Scheduler(tasks, iohandler, plc_obj)
    scheduler.run_tasks()