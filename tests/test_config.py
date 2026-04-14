import os
import unittest
import yaml
from unittest.mock import patch, Mock

from wagoplc.controller import DI
from wagoplc.exceptions import InvalidConfigError
from wagoplc.fb import TON
from wagoplc.read_config import read_config
from wagoplc.tasks import Tasks, Task

def mock_get_controller(controller_id: str):
    return controller_id

@patch("wagoplc.read_config.YAML_CONFIG", "test_controller.yaml")
@patch("wagoplc.read_config.get_controller", Mock(side_effect=mock_get_controller))
class Test_config(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.filename = "test_controller.yaml"
    
    def test_read_non_existing_config_file(self):
        os.remove(self.filename)
        with self.assertRaises(FileNotFoundError):
            read_config()
    
    def test_read_variables(self):
        data = {"itemNumber": "751-9301", "io_mapping": {
            "751-9301": {
                "pii": {"di1": None, "di2": "xSwitch"}, "piq": {"do1": "xMotor"}
            }
            },
            "vars": [{"name": "oPower_on_TON", "fb": "TON"}, {"name": "iStatus", "value": 0}]
        }
        with open(self.filename, "w") as f:
            yaml.dump(data, f)

        _, var_mapping, _ = read_config()
        self.assertListEqual(list(var_mapping.keys()), ["oPower_on_TON", "iStatus", "xSwitch", "xMotor"])
        self.assertIsInstance(var_mapping["xSwitch"], DI)
        self.assertIsInstance(var_mapping["oPower_on_TON"], TON)
        self.assertEqual(var_mapping["iStatus"], 0)

    def test_non_existing_function_block(self):
        data = {"itemNumber": "751-9301", "vars": [{"name": "oHay_To_Gold_FB", "fb": "riches.Hay_To_Gold"}]}
        with open(self.filename, "w") as f:
            yaml.dump(data, f)

        with self.assertRaises(InvalidConfigError) as cm:
            read_config()

        self.assertEqual(str(cm.exception), "No such function block: 'riches.Hay_To_Gold'")

    def test_read_tasks(self):
        data = {"itemNumber": "751-9301", "tasks": [
                {"name": "task1", "entry": "plc.foo", "cycle_ms": None, "priority": None, "watchdog_ms": None, "sensitivity": None},
                ]
        }
        with open(self.filename, "w") as f:
            yaml.dump(data, f)

        with self.assertRaises(InvalidConfigError) as cm:
            read_config()
        self.assertEqual(str(cm.exception), "Function 'plc.foo' for task 'task1' not defined!")

        with open("plc.py", "w") as f:
            f.write("def foo():\n\tpass")

        # Why is this needed?
        os.path.isfile("plc.py")

        tasks, _, plc_obj = read_config()
        self.assertEqual(plc_obj, "751-9301")
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].name, "task1")
        os.remove("plc.py")

    
    def test_missing_task_params(self):
        data = {"itemNumber": "751-9301", "tasks": [
                {"name": "task1", "entry": "plc.py", "cycle_ms": None},
                {"name": "task2", "entry": "plc2.py", "cycle_ms": None, "priority": None, "watchdog_ms": None, "sensitivity": None}
                ]
        }
        with open(self.filename, "w") as f:
            yaml.dump(data, f)
        with self.assertRaises(InvalidConfigError):
            read_config()

    def test_no_itemNumber(self):
        data = {"tasks": [
                {"name": "task2", "entry": "plc2.py", "cycle_ms": None, "priority": None, "watchdog_ms": None, "sensitivity": None}
                ]
        }
        with open(self.filename, "w") as f:
            yaml.dump(data, f)
        with self.assertRaises(InvalidConfigError):
            read_config()

    def test_multiple_io_assignment_exception(self):
        data = {"itemNumber": "751-9301", "io_mapping": {
            "751-9301": {
                "pii": {"di1": "di2"}
            }
        }
        }
        with open("test_controller.yaml", "w") as f:
            yaml.dump(data, f)

        tasks = Tasks()
        @tasks.setup
        def setup():
            di1 = DI(1)
            return locals()

        with self.assertRaises(InvalidConfigError) as cm:
            read_config(tasks)

        self.assertEqual(str(cm.exception), "Duplicate I/O mappings in configuration: {'di2': 'DI(1)', 'di1': 'DI(1)'}")

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.filename)

if __name__ == "__main__":
    unittest.main()