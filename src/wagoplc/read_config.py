"""wagoplc.read_config

Read the configuration file.
- read_config: read and validate the configuration
- validate_task: validate schema of tasks section to
ensure all parameters are present.
"""

from schema import And, Or, Schema, SchemaError, Regex
from typing import Any
import importlib
import logging
import os
import sys
import yaml

from wagoplc.cc100 import CC100_9301, CC100_9401, CC100_9403
from wagoplc.controller import DI, DO, AI, AO, NI, PT, DIO, AIO, IO, Controller
from wagoplc.constants import YAML_CONFIG, INPUT, OUTPUT, LOG_FILE
from wagoplc.exceptions import InvalidConfigError
from wagoplc.tasks import Task, Tasks

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=LOG_FILE,
    format="%(levelname)s - %(asctime)s - %(name)s: %(message)s",
    level=logging.DEBUG
)

def get_controller(controller_id: str) -> Controller:
    """Get controller object by item number.
    
    controller_id: item number
    """
    model, version = controller_id.split("-")
    model = int(model)
    version = int(version)
    
    if model == 751:
        if version == 9301:
            plc_obj = CC100_9301()
        elif version == 9401:
            plc_obj = CC100_9401()
        elif version == 9403:
            plc_obj = CC100_9403()
        plc_obj.init_fds()
    # Inform runtime of controller item number
    with open(".controller-id.txt", "w") as f:
        f.write(controller_id)

    return plc_obj

def read_config(tasks_obj: Tasks | None = None) -> tuple[list[Task], dict[str, Any], Controller]:
    """Read the configuration file.
    
    Return the tasks, the I/O mapping and the controller object.
    Raise FileNotFoundError if the configuration file does not exist.
    Raise InvalidConfigError if the configuration does not include the itemNumber
    field, a function block or a task entry point do not exist, or if there are duplicates
    in the variable mapping.
    """
    if not os.path.exists(YAML_CONFIG):
        raise FileNotFoundError("Configfile does not exist.")
    with open(YAML_CONFIG, "r") as f:
        config = yaml.safe_load(f)
    if not "itemNumber" in config:
        raise InvalidConfigError(f"The field 'itemNumber' is missing.")
    item_number = config["itemNumber"]
    
    # Get state variables
    var_mapping = {}
    if "vars" in config:
        # TODO: Validate schema
        for var in config["vars"]:
            if "fb" in var:
                # Variable is declared as a function block;
                # try to import it.
                try:
                    fb_import = var["fb"].split(".")
                    if len(fb_import) > 1:
                        # fb is in separate module
                        mod_name, func_name = fb_import
                    else:
                        # fb is likely in the standard library
                        mod_name, func_name = "wagoplc.fb", var["fb"]

                    fb_module = sys.modules.get(mod_name, importlib.import_module(mod_name))
                    fb = getattr(fb_module, func_name)
                    # Instantiate the function block
                    value = fb()
                except ImportError, AttributeError:
                    raise InvalidConfigError(f"No such function block: '{var["fb"]}'")
            else:
                # a plain variable with name and value
                value = var["value"]
            var_mapping[var["name"]] = value
    
    # Get task definitions
    tasks = []
    plc_obj = get_controller(item_number)
    logger.info(f"Using controller with item number '{item_number}'")

    # Add decorated task
    if tasks_obj is not None:
        if task := tasks_obj.task:
            task.update({"plc_obj": plc_obj})
            tasks.append(Task(**task))

    if "tasks" in config:
        validate_task(config)
        # Filter out None values
        for task in config["tasks"]:
            # Filter out None values
            task = {k: v for k, v in task.items() if v is not None}
            entry: str = task["entry"]
            module_name, func_name = entry.rsplit(".")
            # Get task definitions from config and retrieve the task function
            try:
                module = importlib.import_module(module_name)
                task["entry"] = getattr(module, func_name)                
                tasks.append(Task(plc_obj, var_mapping, **task))
                logger.debug(f"Task '{task["name"]}' with script entry point '{entry}' registered")
            except ModuleNotFoundError, AttributeError:
                raise InvalidConfigError(f"Function '{entry}' for task '{task["name"]}' not defined!")


    # Get I/O mapping
    if "io_mapping" in config:
        io_mapping = config["io_mapping"]
        for module, sections in io_mapping.items():
            for section_name, section in sections.items():
                if section_name in {"pii", "piq"}:
                    for id, var in section.items():
                        if var:
                            # Separate interface name from number
                            interface = "".join(g for g in id if g.isalpha()) 
                            index = int(id.removeprefix(interface))
                            if interface == "di":
                                var_mapping[var] = DI(index, module)    
                            elif interface == "do":
                                var_mapping[var] = DO(index, module)
                            elif interface == "ai":
                                var_mapping[var] = AI(index, module)
                            elif interface == "ao":
                                var_mapping[var] = AO(index, module)
                            elif interface == "pt":
                                var_mapping[var] = PT(index, module)
                            elif interface == "ni":
                                var_mapping[var] = NI(index, module)
                            elif interface == "dio":
                                # Define type by section name
                                type = INPUT if section_name == "pii" else OUTPUT
                                var_mapping[var] = DIO(index, module, type)
                            elif interface == "aio":
                                type = INPUT if section_name == "pii" else OUTPUT
                                var_mapping[var] = AIO(index, module, type)
    
    if tasks_obj is not None:
        var_mapping.update(tasks_obj.map)
    # Catch duplicate I/O mappings
    vars = list(var_mapping.values())
    duplicate_ios = {
        name: str(value) for name, value in var_mapping.items()
        if isinstance(value, IO) and vars.count(value) > 1
    }
    if duplicate_ios:
        dups_sorted = dict(sorted(duplicate_ios.items(), key=lambda item: item[1]))
        raise InvalidConfigError(f"Duplicate I/O mappings in configuration: {dups_sorted}")

    return tasks, var_mapping, plc_obj

def validate_task(config) -> None:
    "Validate task schema."

    ENTRY_REGEX = r'^[A-Za-z_][A-Za-z0-9_]*\.[A-Za-z_][A-Za-z0-9_]*$'

    task_schema = {
        "name": And(str, len),
        "entry": And(str, Regex(ENTRY_REGEX)),
        "cycle_ms": Or(None, And(int, lambda x: 1 <= x <= 10000)),
        "priority": Or(None, And(int, lambda x: 1 <= x <= 15)),
        "watchdog_ms": Or(None, And(int, lambda x: 1 <= x <= 400000)),
        "sensitivity": Or(None, And(int, lambda x: 0 <= x <= 10)),
    }

    root_schema = Schema({
        "tasks": And(list, lambda lst: len(lst) >= 1, [task_schema])
    })

    try:
        root_schema.validate({"tasks": config["tasks"]})
    except SchemaError as e:
        raise InvalidConfigError(f"The given config is not valid.{e}")
