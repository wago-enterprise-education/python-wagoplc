import os
import unittest
import yaml
from unittest.mock import Mock
from unittest import mock

from wagoplc.fb import TON
from wagoplc.plc import CC100_9301, NotDefinedError, PLC, Task, Tasks
from wagoplc.read_config import read_config, InvalidConfigError
from wagoplc import DI, DO, AI, AO

class Test_config(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.filename = "test_controller.yaml"
    
    @mock.patch("wagoplc.read_config.YAML_CONFIG", "non-existing.yaml")
    def test_read_non_existing_config_file(self):
        with self.assertRaises(FileNotFoundError):
            read_config()
    
    @mock.patch("wagoplc.read_config.YAML_CONFIG", "test_controller.yaml")
    def test_read_variables(self):
        data = {"itemNumber": "751-9301", "io_mapping": {
            "pii": {"x12.di1": None, "x12.di2": "xSwitch"}, "piq": {"x5.do1": "xMotor"}},
            "vars": [{"name": "oPower_on_TON", "fb": "TON"}, {"name": "iStatus", "value": 0}]
        }
        with open(self.filename, "w") as f:
            yaml.dump(data, f)

        _, var_mapping, _ = read_config()
        self.assertListEqual(list(var_mapping.keys()), ["oPower_on_TON", "iStatus", "xSwitch", "xMotor"])
        self.assertIsInstance(var_mapping["xSwitch"], DI)
        self.assertIsInstance(var_mapping["oPower_on_TON"], TON)
        self.assertEqual(var_mapping["iStatus"], 0)

    @mock.patch("wagoplc.read_config.YAML_CONFIG", "test_controller.yaml")
    def test_non_existing_function_block(self):
        data = {"itemNumber": "751-9301", "vars": [{"name": "oHay_To_Gold_FB", "fb": "riches.Hay_To_Gold"}]}
        with open(self.filename, "w") as f:
            yaml.dump(data, f)

        with self.assertRaises(InvalidConfigError) as cm:
            read_config()

        self.assertEqual(str(cm.exception), "No such function block: 'riches.Hay_To_Gold'")

    @mock.patch("wagoplc.read_config.YAML_CONFIG", "test_controller.yaml")
    def test_read_tasks(self):
        data = {"itemNumber": "751-9301", "tasks": [
                {"name": "task1", "entry": "plc.foo", "cycle_ms": None, "priority": None, "watchdog_ms": None, "sensitivity": None},
                {"name": "task2", "entry": "plc2.bar", "cycle_ms": None, "priority": None, "watchdog_ms": None, "sensitivity": None}
                ]
        }
        with open(self.filename, "w") as f:
            yaml.dump(data, f)

        tasks, _, itemNum = read_config()
        self.assertEqual(itemNum, "751-9301")
        self.assertListEqual(tasks, [
            {"name": "task1", "entry": "plc.foo"},
            {"name": "task2", "entry": "plc2.bar"}        
        ])

    
    @mock.patch("wagoplc.read_config.YAML_CONFIG", "test_controller.yaml")
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

    @mock.patch("wagoplc.read_config.YAML_CONFIG", "test_controller.yaml")
    def test_no_itemNumber(self):
        data = {"tasks": [
                {"name": "task2", "entry": "plc2.py", "cycle_ms": None, "priority": None, "watchdog_ms": None, "sensitivity": None}
                ]
        }
        with open(self.filename, "w") as f:
            yaml.dump(data, f)
        with self.assertRaises(InvalidConfigError):
            read_config()

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.filename)


class Test_PLC(unittest.TestCase):
    
    def test_get_controller(self):
        pass
    
    @mock.patch("wagoplc.read_config.YAML_CONFIG", "test_controller.yaml")
    def test_read_task_config(self):
        data = {"itemNumber": "751-9301", "tasks": [
            {"name": "foo", "entry": "foo.bar", "cycle_ms": 10, "priority": 1, "sensitivity": None, "watchdog_ms": None}
        ]}

        with open("test_controller.yaml", "w") as f:
            yaml.dump(data, f)

        with open("foo.py", "w") as f:
            f.write(
"""
def bar():
    return locals()
"""
            )
                
        tasks = Tasks()
        @tasks.register(
            name="foo",
            cycle_ms=10,
            priority=1
        )
        def foo():
            return locals()

        plc = PLC(tasks)
        for task in plc.tasks:
            self.assertEqual(task.name, "foo")
            self.assertDictEqual(task.cycle_func(), {})
            self.assertEqual(task.cycle_ms, 10)
            self.assertEqual(task.priority, 1)

        os.remove("test_controller.yaml")
        os.remove("foo.py")

    @mock.patch("wagoplc.read_config.YAML_CONFIG", "test_controller.yaml")
    def test_multiple_io_assignment_exception(self):
        data = {"itemNumber": "751-9301"}
        with open("test_controller.yaml", "w") as f:
            yaml.dump(data, f)

        tasks = Tasks()
        @tasks.setup
        def setup():
            di1 = DI(1)
            di2 = DI(1)
            return locals()

        with self.assertRaises(InvalidConfigError) as cm:
            PLC(tasks)

        self.assertEqual(str(cm.exception), "Duplicate I/O mappings in configuration: {'di1': 'DI(1)', 'di2': 'DI(1)'}")

class Test_Tasks(unittest.TestCase):

    def test_setup_error_on_missing_return(self):
        tasks = Tasks()
        def setup():
            xFan = DO(1)

        with self.assertRaises(InvalidConfigError) as cm:
            tasks.setup(setup)

        self.assertEqual(str(cm.exception), "Expected setup function to return a dictionary of variables!")

    def test_task_register(self):
        tasks = Tasks()
        @tasks.register(name="foo")
        def foo():
            pass

        self.assertEqual(tasks.task.cycle_func, foo)
        self.assertEqual(tasks.task.name, "foo")

        with self.assertRaises(InvalidConfigError) as cm:
            @tasks.register
            def bar(foo):
                print(foo)

        self.assertEqual(str(cm.exception), "Only one task per program allowed!")

    def test_task_register_no_config(self):
        tasks = Tasks()
        @tasks.register
        def foo():
            pass

        self.assertEqual(tasks.task.cycle_func, foo)


class Test_Task(unittest.TestCase):
    
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
                var_mapping=io_map,
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

        io_map = {"a": DO(1)}  # b missing
        cc_obj = CC100_9301()

        with self.assertRaises(NotDefinedError):
            Task(cc_obj, io_map, "BadTask", entry=f)

    def test_get_outputs(self):
        io_map = {
            "a": DO(1),
            "b": DO(2),
            "c": AO(2),
            "d": DI(4),
        }

        t = Task(
            cc_obj=CC100_9301(),
            var_mapping=io_map,
            name="OutputTest",
            entry=lambda a, b: {"b": 1}
        )

        self.assertSetEqual(set(t.outputs.keys()), {"a", "b", "c"})

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
        t = Task(CC100_9301(),var_mapping=dict(),name="test",entry=cycle_func_returns_none)
        
        with self.assertRaises(NotDefinedError):
            t.cycle(read_fds={},write_fds={},state_vars={})

    def test_cycle_with_state_vars(self):
        def cycle_func(iStatus: int):
            iStatus = 1
            return dict(iStatus=iStatus)

        t = Task(CC100_9301(), var_mapping={"iStatus": 0}, name="test", entry=cycle_func)
        state_vars = t.cycle(read_fds={}, write_fds={}, state_vars={})
        self.assertDictEqual(state_vars, {"iStatus": 1})

if __name__ == '__main__':
        unittest.main()