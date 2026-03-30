from unittest.mock import Mock
import unittest

from wagoplc.controller import DI, DO, AO
from wagoplc.exceptions import NotDefinedError, InvalidConfigError
from wagoplc.tasks import Task, Tasks

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

        self.assertEqual(tasks.task["entry"], foo)
        self.assertEqual(tasks.task["name"], "foo")

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
        self.assertEqual(tasks.task["entry"], foo)


class Test_Task(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        plc_obj_mock = Mock()
        plc_obj_mock.input_image = {}
        plc_obj_mock.output_image = {}
        plc_obj_mock.read_inputs.return_value = None
        plc_obj_mock.write_outputs.return_value = None
        cls.plc_obj_mock = plc_obj_mock
    
    def test_init_with_callable(self):
            def dummy_func(a, b):
                return {"x": 1}

            io_map = {
                "a": DI(1),
                "b": DI(2),
                "x": DO(3),
            }

            t = Task(
                plc_obj=None,
                var_mapping=io_map,
                name="TestTask",
                cycle_ms=100,
                priority=5,
                entry=dummy_func
            )

            self.assertEqual(t.cycle_func, dummy_func)
            self.assertEqual(t.priority, 5)
            self.assertSetEqual(set(t.iohandler.inputs.keys()), {"a", "b"})
            self.assertSetEqual(set(t.iohandler.outputs.keys()), {"x"})

    def test_get_inputs_fails_on_missing_vars(self):
        def f(a, b):
            return {}

        io_map = {"a": DO(1)}  # b missing

        with self.assertRaises(NotDefinedError):
            Task(None, io_map, "BadTask", entry=f)

    def test_get_outputs(self):
        io_map = {
            "a": DO(1),
            "b": DO(2),
            "c": AO(2),
            "d": DI(4),
        }

        t = Task(
            plc_obj=None,
            var_mapping=io_map,
            name="OutputTest",
            entry=lambda a, b: {"b": 1}
        )

        self.assertSetEqual(set(t.iohandler.outputs.keys()), {"a", "b", "c"})

    def test_priority_compare(self):
        t1 = Task(None, {}, "T1", entry=lambda: None, priority=5)
        t2 = Task(None, {}, "T2", entry=lambda: None, priority=10)

        self.assertTrue(t1 < t2)
        self.assertFalse(t2 < t1)

    def test_priority_out_of_range(self):
        with self.assertRaises(ValueError):
            Task(None, {}, "BadPrio", entry=lambda: None, priority=0)

        with self.assertRaises(ValueError):
            Task(None, {}, "BadPrio", entry=lambda: None, priority=16)

    def test_sensitivity_out_of_range(self):
        with self.assertRaises(ValueError):
            Task(None, {}, "BadSens", entry=lambda: None, sensitivity=11)
 
    def test_cycle_raises_if_cycle_func_returns_none(self):
        def cycle_func_returns_none():
            return None
        t = Task(self.plc_obj_mock,var_mapping=dict(),name="test",entry=cycle_func_returns_none)
        
        with self.assertRaises(NotDefinedError):
            t.cycle()

    def test_cycle_with_state_vars(self):

        def cycle_func(iStatus: int):
            iStatus = 1
            return dict(iStatus=iStatus)

        t = Task(self.plc_obj_mock, var_mapping={"iStatus": 0}, name="test", entry=cycle_func)
        t.cycle()
        self.assertDictEqual(t.iohandler.state_vars, {"iStatus": 1})

if __name__ == '__main__':
        unittest.main()