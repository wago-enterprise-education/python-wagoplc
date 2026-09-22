import unittest

from unittest.mock import Mock
from wagoplc.controller import IOHandler
from wagoplc.controller import DI, AI, DO
from wagoplc.exceptions import NotDefinedError
from wagoplc.tasks import Task

class DummyController:
    def read_inputs(self):
        pass

    def write_outputs(self):
        pass

    def digitalRead(self, *_): pass
    def analogRead(self, *_): pass
    def tempRead(self, *_): pass

    def digitalWrite(self, *_): pass
    def analogWrite(self, *_): pass

class TestIOHandler(unittest.TestCase):

    def setUp(self):
        self.plc = DummyController()

        var_mapping = {
            "xDI1": DI(id=1, module=0),
            "xAI1": AI(id=2, module=0),
            "var": 42,
            "xDO1": DO(id=10, module=0),
        }

        self.handler = IOHandler(
            plc_object=self.plc,
            var_mapping=var_mapping
        )

        # hardware mock
        self.handler.read = Mock(return_value=0)
        self.handler.write = Mock()

    def test_input_variable_in_output_image_raises_error(self):
        output_image = {
            "xDI1": True
        }
        def foo(xDI1):
            pass
        t = Task("task", foo)
        self.handler.set_task_vars(t)

        with self.assertRaises(ValueError):
            self.handler.process_output_image(t, output_image)

    def test_valid_output_is_written(self):
        output_image = {
            "xDO1": True
        }
        def foo():
            pass
        t = Task("task", foo)
        self.handler.set_task_vars(t)

        self.handler.process_output_image(t, output_image)
        self.handler.write.assert_called_once()

    def test_state_variable_is_allowed(self):
        output_image = {
            "var": 2
        }
        def foo():
            pass
        t = Task("task", foo)
        self.handler.set_task_vars(t)

        self.handler.process_output_image(t, output_image)
        self.assertEqual(t.state_vars["var"], 2)

    def test_set_state_vars(self):
        t = Task(
            name="task",
            entry=lambda var: {}
        )
        self.handler.set_task_vars(t)
        self.assertDictEqual(t.state_vars, {"var": 42})


    def test_set_state_vars_fails_on_missing_vars(self):
        def f(var, foo):
            return {}

        with self.assertRaises(NotDefinedError):
            t = Task("BadTask", entry=f)
            self.handler.set_task_vars(t)

    def test_get_outputs(self):
        t = Task(
            name="OutputTest",
            entry=lambda xDI1, xDO1: {"xDO1": True, "var": 1}
        )
        self.handler.set_task_vars(t)

        self.assertSetEqual(set(self.handler.outputs.keys()), {"xDO1"})



if __name__ == "__main__":
    unittest.main()