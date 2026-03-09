import yaml
import os
from schema import Schema,SchemaError,And,Regex,Or
from wagoplc.cc100.cc100_v1 import DI, DO, AI, AO
from wagoplc.cc100.constants import YAML_CONFIG

class InvalidConfig(Exception):
    """Throw when an invalid configuration was given."""
    pass

def read_config() -> tuple[list, dict, str]:
    """Read the configuration file.
    
    Return the tasks, the I/O mapping and the item number.
    """
    if not os.path.exists(YAML_CONFIG):
        raise FileNotFoundError("Configfile does not exist.")
    with open(YAML_CONFIG, "r") as f:
        config = yaml.safe_load(f)
    if not "itemNumber" in config:
        raise InvalidConfig(f"No ItemNumber was given.")
    
    tasks = []
    if "tasks" in config:
        validate_task(config)
        # Filter out None values
        for task in config["tasks"]:
            # Filter out None values
            tasks.append(dict(filter(
                lambda p: p[1] is not None, task.items()
            )))

    result = {}
    if "io_mapping" in config:
        io_mapping = config["io_mapping"]
        for section in io_mapping.values():           
            for full_key, value in section.items():   
                if value:                             
                    short_key = full_key.split(".", 1)[1] 
                    interface = short_key[:2]
                    index = int(short_key[2])
                    if interface == "di":
                        result[value] = DI(index)    
                    elif interface == "do":
                        result[value] = DO(index)
                    elif interface == "ai":
                        result[value] = AI(index)
                    elif interface == "ao":
                        result[value] = AO(index)

    return tasks, result, config["itemNumber"]

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
        raise InvalidConfig(f"The given config is not valid.{e}")