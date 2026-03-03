import yaml

from wagoplc.cc100.cc100_v1 import DI, DO, AI, AO
from wagoplc.cc100.constants import YAML_CONFIG
def read_config():
    with open(YAML_CONFIG, "r") as f:
        config = yaml.safe_load(f)

    io_mapping = config["io_mapping"]

    result = {}

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



    return config["tasks"],result


r= read_config()
print(r)
    
    
    