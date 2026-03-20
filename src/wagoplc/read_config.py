from schema import And, Or, Schema, SchemaError, Regex
from typing import Any
import importlib
import os
import sys
import yaml

from wagoplc.controller import DI, DO, AI, AO, NI, PT, DIO, AIO
from wagoplc.constants import YAML_CONFIG

class InvalidConfigError(Exception):
    """Throw when an invalid configuration was given."""
    pass

def read_config() -> tuple[list[dict[str, int | str]], dict[str, Any], str]:
    """Read the configuration file.
    
    Return the tasks, the I/O mapping and the item number.
    """
    if not os.path.exists(YAML_CONFIG):
        raise FileNotFoundError("Configfile does not exist.")
    with open(YAML_CONFIG, "r") as f:
        config = yaml.safe_load(f)
    if not "itemNumber" in config:
        raise InvalidConfigError(f"No ItemNumber was given.")
    
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
    
    tasks = []
    if "tasks" in config:
        validate_task(config)
        # Filter out None values
        for task in config["tasks"]:
            # Filter out None values
            tasks.append(dict(filter(
                lambda p: p[1] is not None, task.items()
            )))

    if "io_mapping" in config:
        io_mapping = config["io_mapping"]
        for module,sections in io_mapping.items():           
            for sections_name, section in section.items():   
                if sections_name in {"pii","piq"}:
                    for key, value in sections.items():
                        if value: 
                            interface = "".join(g for g in key if g.isalpha)  
                            index = "".join(g for g in key if g.isdigit)                 
                            if interface == "di":
                                var_mapping[value] = DI(module,index)    
                            elif interface == "do":
                                var_mapping[value] = DO(module,index)
                            elif interface == "ai":
                                var_mapping[value] = AI(module,index)
                            elif interface == "ao":
                                var_mapping[value] = AO(module,index)
                            elif interface == "pt":
                                var_mapping[value] = PT(module,index)
                            elif interface == "ni":
                                var_mapping[value] = NI(module,index)
                            elif interface == "dio":
                                type = 0 if sections == "pii" else 1
                                var_mapping[value] = DIO(module,index,type)
                            elif interface == "aio":
                                type = 0 if sections == "pii" else 1
                                var_mapping[value] = AIO(module,index,type)

    return tasks, var_mapping, config["itemNumber"]

def validate_task(config):
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
