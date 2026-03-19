import os
import unittest

from pyfakefs import fake_filesystem_unittest

from wagoplc.cc100.cc100_v1 import CC100_v1, DI, DO
from wagoplc.cc100.cc100_9403 import CC100_9403
from wagoplc.cc100.exceptions import NonExistingIOError

TEST_CALIB_DATA = """PT1 PT2 AI1 AI2 A01 A02
12452 1182 21785 1777
12402 1179 21767 1788
5898 1025 50375 9022
5698 990 50205 8997
1064 350 8976 3000
1053 350 8966 3000
"""

class Test_CC100_v1(fake_filesystem_unittest.TestCase):
    @classmethod
    @unittest.mock.patch("wagoplc.cc100.cc100_v1.TEST_DATA", "")
    def setUpClass(cls):
        cls.setUpClassPyfakefs()
        cls.cc = CC100_v1()

        # create files and directories
        for path in cls.cc.get_read_paths() + cls.cc.get_read_once_paths():
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                f.write("0")

        for path in cls.cc.get_write_paths():
            os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(cls.cc.CALIB_DATA, "w") as f:
            f.write(TEST_CALIB_DATA)

        cls.cc.input_image[cls.cc.CALIB_DATA] = TEST_CALIB_DATA
        cls.cc.input_image[cls.cc.DOUT_DATA] = "0"

        cls.cc.init_fds()
        # Initially read inputs
        cls.cc.read_inputs()

    def test_non_existing_output(self):
        with self.assertLogs(level="WARNING") as cm:
            self.assertFalse(self.cc.digitalWrite(5, True))
            self.assertFalse(self.cc.analogWrite(3, 1000))
        self.assertEqual(
            cm.output,
            [
                "WARNING:wagoplc.cc100.cc100_v1:Digital output does not exist",
                "WARNING:wagoplc.cc100.cc100_v1:Analog output does not exist"
            ]
        )

    def test_digital_write(self):
        # set every digital output to False and True
        dout_content = 0
        for i in range(1, 5):
            for j in range(2):
                self.assertTrue(self.cc.digitalWrite(i, j))
                # file content increases by power of two
                dout_content += 2**(i - 1) * j
                self.assertEqual(self.cc.output_image[self.cc.DOUT_DATA], str(dout_content))
                self.cc.write_outputs()

    def test_non_existing_input(self):
        with self.assertLogs(level="WARNING") as cm:
                self.assertFalse(self.cc.digitalRead(9))
                self.assertFalse(self.cc.analogRead(3))
        self.assertEqual(
            cm.output,
            [
                "WARNING:wagoplc.cc100.cc100_v1:Digital input does not exist",
                "WARNING:wagoplc.cc100.cc100_v1:Analog input does not exist"
            ]
        )
              
    def test_digital_read(self):
        for i in range(1, 9):
            # Simulate digital input
            with open(self.cc.DIN, "w") as din:
                din.write(str(2**(i - 1)))
            self.assertFalse(self.cc.digitalRead(i))
            self.cc.read_inputs()
            self.assertTrue(self.cc.digitalRead(i))

    def test_analog_write(self):
        for i in range(1, 3):
            for j in range(0,10001,1000):
                self.assertTrue(self.cc.analogWrite(i,j))
        
    def test_analog_read(self):
        for i in range(1,3):
            self.cc.analogRead(i)

    def test_read_inputs(self):
        inputs = {"di1": DI(1)}
        input_image = {"di1": True}
        with open(self.cc.DIN, "w") as din:
            din.write("1")
        self.assertDictEqual(
            self.cc.read_inputs(input_mapping=inputs),
            input_image
        )
        self.assertEqual(self.cc.input_image[self.cc.DIN], "1")

    def test_write_outputs(self):
        outputs = {"do1": DO(1)}
        output_image = {"do1": True}
        # reset input value
        self.cc.input_image[self.cc.DOUT_DATA] = "0"

        self.cc.digitalWrite(1, True)
        self.cc.write_outputs(
            output_image=output_image,
            outputs=outputs
        )
        # value was directly written to input image
        self.assertEqual(self.cc.input_image[self.cc.DOUT_DATA], "1")
        
    def test_temp_read(self):
        pass

    def test_analog_read_error_9403(self):
        cc = CC100_9403()
        with self.assertRaises(NonExistingIOError) as io:
            cc.analogRead(1)

        self.assertEqual(str(io.exception),"The 751-9403 has no analog inputs.")

    def test_reset(self):
        self.cc.reset()
        self.assertTrue(all(out == "0" for out in self.cc.output_image.values()))
 
if __name__ == "__main__":
    unittest.main()