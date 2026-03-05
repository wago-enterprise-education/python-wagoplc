import os
import unittest

from pyfakefs import fake_filesystem_unittest

from wagoplc.cc100.cc100_v1 import CC100_v1, DI, DO
from wagoplc.cc100.constants import DOUT_DATA, DIN, CALIB_DATA

TEST_CALIB_DATA = """PT1 PT2 AI1 AI2 A01 A02
12452 1182 21785 1777
12402 1179 21767 1788
5898 1025 50375 9022
5698 990 50205 8997
1064 350 8976 3000
1053 350 8966 3000
"""
cc = CC100_v1()

class Test_CC100_v1(fake_filesystem_unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.setUpClassPyfakefs()

        # create files and directories
        for path in cc.get_read_paths() + cc.get_read_once_paths():
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                f.write("0")

        for path in cc.get_write_paths():
            os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(CALIB_DATA, "w") as f:
            f.write(TEST_CALIB_DATA)

        cc.input_image[CALIB_DATA] = TEST_CALIB_DATA
        cc.input_image[DOUT_DATA] = "0"

        cls.read_fds = {path: open(path, "r") for path in cc.get_read_paths()}
        cls.write_fds = {path: open(path, "w") for path in cc.get_write_paths()}

        # Initially read inputs
        cc.read_inputs(cls.read_fds)

    def test_non_existing_output(self):
        with self.assertLogs(level="WARNING") as cm:
            self.assertFalse(cc.digitalWrite(5, True))
            self.assertFalse(cc.analogWrite(3, 1000))
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
                self.assertTrue(cc.digitalWrite(i, j))
                # file content increases by power of two
                dout_content += 2**(i - 1) * j
                self.assertEqual(cc.output_image[DOUT_DATA], str(dout_content))
                cc.write_outputs(self.write_fds)

    def test_non_existing_input(self):
        with self.assertLogs(level="WARNING") as cm:
                self.assertFalse(cc.digitalRead(9))
                self.assertFalse(cc.analogRead(3))
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
            with open(DIN, "w") as din:
                din.write(str(2**(i - 1)))
            self.assertFalse(cc.digitalRead(i))
            cc.read_inputs(self.read_fds)
            self.assertTrue(cc.digitalRead(i))

    def test_analog_write(self):
        for i in range(1, 3):
            for j in range(0,10001,1000):
                self.assertTrue(cc.analogWrite(i,j))
        
    def test_analog_read(self):
        for i in range(1,2):
            cc.analogRead(i)

    def test_read_inputs(self):
        inputs = {"di1": DI(1)}
        input_image = {"di1": True}
        with open(DIN, "w") as din:
            din.write("1")
        self.assertDictEqual(
            cc.read_inputs(fds=self.read_fds, io_mapping=inputs),
            input_image
        )
        self.assertEqual(cc.input_image[DIN], "1")

    def test_write_outputs(self):
        outputs = {"do1": DO(1)}
        output_image = {"do1": True, "di1": True}
        # reset input value
        cc.input_image[DOUT_DATA] = "0"

        cc.digitalWrite(1, True)
        cc.write_outputs(
            fds=self.write_fds,
            output_image=output_image,
            outputs=outputs
        )
        # value was directly written to input image
        self.assertEqual(cc.input_image[DOUT_DATA], "1")
        
    def test_temp_read(self):
        pass

    def test_reset_outputs(self):
        cc.reset_outputs(self.write_fds)
        self.assertTrue(all(out == "0" for out in cc.output_image.values()))

if __name__ == '__main__':
    unittest.main()
