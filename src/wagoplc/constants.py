"""
Top-level constants.
"""
import os
# path of controller configuration
YAML_CONFIG = "controller.yaml"
LOG_FILE = "/var/log/wago/python_bootapplication.log" if os.path.exists("/var/log/wago/") else "wagoplc.log"

# main PLC script
SCRIPT_PATH = "/home/user/python_bootapplication/"
PLC_SCRIPT = "plc_prg"

#read_config variable IOs
INPUT = 0
OUTPUT = 1