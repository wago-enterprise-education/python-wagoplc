import unittest
from unittest.mock import Mock
from wagoplc.controller import IOHandler
from wagoplc.controller import DI, AI, PT, NI, DO, AO

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

        input_mapping = {
            "xDI1": DI(id=1, module=0),
            "xAI1": AI(id=2, module=0),
            "var": 42,
        }

        var_mapping = {
            "xDO1": DO(id=10, module=0),
        }

        self.handler = IOHandler(
            plc_object=self.plc,
            input_mapping=input_mapping,
            var_mapping=var_mapping,
        )

        # hardware mock
        self.handler.read = Mock(return_value=0)
        self.handler.write = Mock()

        # input vars 
        self.handler.get_input_image()

    def test_input_variable_in_output_image_raises_error(self):
        output_image = {
            "xDI1": 1
        }

        with self.assertRaises(ValueError):
            self.handler.process_output_image(output_image)

    def test_valid_output_is_written(self):
        output_image = {
            "xDO1": True
        }

        self.handler.process_output_image(output_image)

        self.handler.write.assert_called_once()

    def test_state_variable_is_allowed(self):
        output_image = {
            "var": 2
        }

        self.handler.process_output_image(output_image)

        self.assertEqual(self.handler.state_vars["var"], 2)


if __name__ == "__main__":
    unittest.main()