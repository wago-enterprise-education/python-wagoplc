from unittest.mock import Mock
import unittest

from wagoplc.controller import DI, DO, IOHandler
from wagoplc.tasks import Task

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
                name="TestTask",
                cycle_ms=100,
                priority=5,
                entry=dummy_func
            )

            iohandler = IOHandler(self.plc_obj_mock, io_map)
            iohandler.set_task_vars(t)

            self.assertEqual(t.cycle_func, dummy_func)
            self.assertEqual(t.priority, 5)
            self.assertSetEqual(set(t.inputs.keys()), {"a", "b"})

    def test_priority_compare(self):
        t1 = Task("T1", entry=lambda: None, priority=5)
        t2 = Task("T2", entry=lambda: None, priority=10)

        self.assertTrue(t1 < t2)
        self.assertFalse(t2 < t1)

    def test_priority_out_of_range(self):
        with self.assertRaises(ValueError):
            Task("BadPrio", entry=lambda: None, priority=0)

        with self.assertRaises(ValueError):
            Task("BadPrio", entry=lambda: None, priority=16)

    def test_sensitivity_out_of_range(self):
        with self.assertRaises(ValueError):
            Task("BadSens", entry=lambda: None, sensitivity=11)

if __name__ == '__main__':
        unittest.main()