import os
import unittest
import yaml
import types
import importlib
from unittest.mock import Mock, patch
from unittest import mock


from wagoplc.plc import NotDefinedError, Task, PLC, CC100_9301
from wagoplc.read_config import read_config,InvalidConfig
from wagoplc import DI, DO, AI, AO

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


class Test_plc(unittest.TestCase):
    
    def test_get_controller(self):
        pass

    def test_setup(self):
        pass

    def test_task(self):
        pass
        

class Test_Task(unittest.TestCase):
    
    def test_get_inputs(self):
        pass

    def test_get_outputs(self):
        pass

    def test_init(self):
        pass
        #Task.__init__(self,cc_obj=CC100_9301,io_mapping=dict(),name="test",)


    
    
    def test_init_with_callable(self):
            def dummy_func(a, b):
                return {"x": 1}

            io_map = {
                "a": DI(1),
                "b": DI(2),
                "x": DO(3),
            }

            cc_obj = CC100_9301()

            t = Task(
                cc_obj=cc_obj,
                io_mapping=io_map,
                name="TestTask",
                cycle_ms=100,
                priority=5,
                entry=dummy_func
            )

            self.assertEqual(t.cycle_func, dummy_func)
            self.assertEqual(t.priority, 5)
            self.assertSetEqual(set(t.inputs.keys()), {"a", "b"})
            self.assertSetEqual(set(t.outputs.keys()), {"x"})

    def test_get_inputs_fails_on_missing_vars(self):
        def f(a, b):
            return {}

        io_map = {"a": DO(1)}  # b fehlt
        cc_obj = CC100_9301()

        with self.assertRaises(NotDefinedError):
            Task(cc_obj, io_map, "BadTask", entry=f)

    def test_get_outputs_filters_correctly(self):
        io_map = {
            "a": DO(1),
            "b": DO(2),
            "c": AO(2),
            "d": DI(4),
        }

        t = Task(
            cc_obj=CC100_9301(),
            io_mapping=io_map,
            name="OutputTest",
            entry=lambda a, b: {"b": 1}
        )

        self.assertSetEqual(set(t.outputs.keys()), {"a","b", "c"})

    def test_priority_compare(self):
        t1 = Task(Mock(), {}, "T1", entry=lambda: None, priority=5)
        t2 = Task(Mock(), {}, "T2", entry=lambda: None, priority=10)

        self.assertTrue(t1 < t2)
        self.assertFalse(t2 < t1)

    def test_priority_out_of_range(self):
        with self.assertRaises(ValueError):
            Task(CC100_9301(), {}, "BadPrio", entry=lambda: None, priority=0)

        with self.assertRaises(ValueError):
            Task(CC100_9301(), {}, "BadPrio", entry=lambda: None, priority=16)

    def test_sensitivity_out_of_range(self):
        with self.assertRaises(ValueError):
            Task(CC100_9301(), {}, "BadSens", entry=lambda: None, sensitivity=11)
 
    def test_cycle_raises_if_cycle_func_returns_none(self):

        def cycle_func_returns_none():
            return None
        t = Task(CC100_9301,io_mapping=dict(),name="test",entry=cycle_func_returns_none)
        
        with self.assertRaises(NotDefinedError):
            t.cycle(read_fds={},write_fds={})

if __name__ == '__main__':
        unittest.main()