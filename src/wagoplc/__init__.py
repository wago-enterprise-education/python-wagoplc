from wagoplc.plc import Tasks, PLC, DI, DO, AI, AO

def main(tasks_object: Tasks | None = None):
    """
    Main runtime loop to run the given tasks in cycles.
    """
    plc = PLC(tasks_object)
    task = plc.tasks[0]
    plc.run_tasks()