from unittest import mock

import os
import unittest
import yaml

from wagoplc.plc import PLC,Task
from wagoplc.read_config import read_config,InvalidConfig
from wagoplc.cc100.constants import YAML_CONFIG

r = PLC()
class Test_config(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.filename = "test_controller.yaml"
    
    @mock.patch("wagoplc.read_config.YAML_CONFIG", "non-existing.yaml")
    def test_read_non_existing(self):
        with self.assertRaises(FileNotFoundError):
            read_config()
    
    @mock.patch("wagoplc.read_config.YAML_CONFIG", "test_controller.yaml")
    def test_read_yaml(self):
        data = {"itemNumber": "751-9301", "tasks": [
                {"name":"task1","entry":"plc.py","cycle_ms":None,"priority":None,"watchdog_ms":None,"sensitivity":None},
                {"name":"task2","entry":"plc2.py","cycle_ms":None,"priority":None,"watchdog_ms":None,"sensitivity":None}
                ]}
        with open(self.filename, "w") as f:
            yaml.dump(data, f)
        with open(self.filename, "r") as f:
            loaded = yaml.safe_load(f)
        self.assertEqual(loaded["itemNumber"], "751-9301")
        n= read_config()
        a,b,c = n
        self.assertEqual(loaded["itemNumber"],c)
        self.assertEqual(loaded["tasks"],a)
    
    @mock.patch("wagoplc.read_config.YAML_CONFIG", "test_controller.yaml")
    def test_invalid_config(self):
        data = {"itemNumber": "751-9301", "tasks": [
                {"name":"task1","entry":"plc.py","cycle_ms":None},
                {"name":"task2","entry":"plc2.py","cycle_ms":None,"priority":None,"watchdog_ms":None,"sensitivity":None}
                ]}
        with open(self.filename, "w") as f:
            yaml.dump(data, f)
        with self.assertRaises(InvalidConfig):
            read_config()
    @mock.patch("wagoplc.read_config.YAML_CONFIG", "test_controller.yaml")
    def test_no_itemNumber(self):
        data = {"tasks":[
                {"name":"task2","entry":"plc2.py","cycle_ms":None,"priority":None,"watchdog_ms":None,"sensitivity":None}
                ]}
        with open(self.filename, "w") as f:
            yaml.dump(data, f)
        with self.assertRaises(InvalidConfig):
            read_config()

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.filename)


if __name__ == '__main__':
    unittest.main()
    