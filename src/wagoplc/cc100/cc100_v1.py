from io import TextIOWrapper
import logging
import os

from wagoplc.controller import Controller, DI, DO, AI, AO, PT

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="wagoplc.log",
    format="%(levelname)s - %(asctime)s - %(name)s: %(message)s",
    level=logging.DEBUG
)

TEST_DATA = os.getenv("TESTDATA", os.getcwd() + "/test_data")

class CC100_v1(Controller):
    # data paths on CC100 751-9301 (V1)
    DOUT_DATA ="/sys/kernel/dout_drv/DOUT_DATA"
    OUT_VOLTAGE1_POWERDOWN = "/sys/bus/iio/devices/iio:device0/out_voltage1_powerdown"
    OUT_VOLTAGE2_POWERDOWN = "/sys/bus/iio/devices/iio:device1/out_voltage2_powerdown"
    OUT_VOLTAGE1_RAW = "/sys/bus/iio/devices/iio:device0/out_voltage1_raw"
    OUT_VOLTAGE2_RAW = "/sys/bus/iio/devices/iio:device1/out_voltage2_raw"
    DIN = "/sys/devices/platform/soc/44009000.spi/spi_master/spi0/spi0.0/din"
    IN_VOLTAGE3_RAW = "/sys/bus/iio/devices/iio:device3/in_voltage3_raw"
    IN_VOLTAGE0_RAW = "/sys/bus/iio/devices/iio:device3/in_voltage0_raw"
    IN_VOLTAGE13_RAW = "/sys/bus/iio/devices/iio:device2/in_voltage13_raw"
    IN_VOLTAGE1_RAW = "/sys/bus/iio/devices/iio:device2/in_voltage1_raw"
    CALIB_DATA = "/etc/calib"
    SERIAL_PORT = "/dev/ttySTM1"

    def __init__(self):
        self.item_num: int
        self.file_map = {
            "pii": {
                DI: self.DIN,
                AI: {
                    1: self.IN_VOLTAGE3_RAW, 2: self.IN_VOLTAGE0_RAW
                },
                PT: {
                    1: self.IN_VOLTAGE13_RAW, 2: self.IN_VOLTAGE1_RAW
                }
            },
            "piq": {
                DO: self.DOUT_DATA,
                AO: {
                    1: self.OUT_VOLTAGE1_RAW, 2: self.OUT_VOLTAGE2_RAW,
                    "1_power": self.OUT_VOLTAGE1_POWERDOWN,
                    "2_power": self.OUT_VOLTAGE2_POWERDOWN 
                }
            },
            "read_once": {
                "calib": self.CALIB_DATA,
                DO: self.DOUT_DATA
            }
        }
        self.specs = {
            DI: 8,
            AI: 2,
            PT: 2,
            DO: 4,
            AO: 2
        }

        self.input_data: dict[str, str] = {self.item_num: {"specs": self.specs, AI: {}, PT: {}}}
        # Add all output paths to output image for reset
        self.output_data: dict[str, str] = {self.item_num: {AO: {}}}

    def init_fds(self):
        """Get system file descriptors for the CC100 v1."""
        self._read_fds: dict[str, TextIOWrapper] = {}
        self._write_fds: dict[str, TextIOWrapper] = {}
        
        for loc in self.file_map["pii"].values():
            if isinstance(loc, dict):
                for path in loc.values():
                    self._read_fds[path] = open(TEST_DATA + path, "r")
            else:
                self._read_fds[loc] = open(TEST_DATA + loc, "r")

        # Read digital output file initially and add it to the input image.
        # The value is updated after every write, the file is kept open
        # in write mode.  Otherwise, it would be necessary to use update file mode
        # (r+), which is too costly.
        for key, loc in self.file_map["read_once"].items():
            with open(TEST_DATA + loc, "r") as f:
                self.input_data[key] = f.read()

        for loc in self.file_map["piq"].values():
            if isinstance(loc, dict):
                for path in loc.values():
                    self._write_fds[path] = open(TEST_DATA + path, "w")
            else:
                self._write_fds[loc] = open(TEST_DATA + loc, "w")

    def analogWrite(self, output: int, voltage: int, module: str) -> bool:
        """Switch the output to the specified voltage.

        Return False if analog output does not exist,
        else return True.
        
        output: Analog output to be switched
        voltage: Voltage which the selected output should be set to
        """
        if output == 1:
            self.output_data[self.item_num][AO]["1_power"] = "0"
        elif output == 2:
            self.output_data[self.item_num][AO]["2_power"] = "0"
        super().analogWrite(output, voltage, module)

    # Output calibration from: https://github.com/WAGO/cc100-howtos/blob/main/HowTo_Access_Onboard_IO/accessIO_CC100.py
    def getCalibrationData(self, value: int) -> list[str]:
        """Return the calibration data for the required row of the table.

        value: the row to read
        """
        calib_data = self.input_data["calib"].strip().split("\n")[1:]
        return calib_data[value].rstrip().split(' ', 4)

    def calcCalibrate(self, val_uncal: int, calib: int)-> int:
        """Calculate the value of the voltage for the required output.

        val_uncal: uncalibrated value
        calib: calibration data
        """
        x1=int(calib[0])
        y1=int(calib[1])
        x2=int(calib[2])
        y2=int(calib[3])

        val_cal=(y2-y1)*int(val_uncal-x1)
        val_cal=val_cal/(x2-x1)
        val_cal=val_cal+y1

        return int(val_cal)
    
    def calibrateOut(self, voltage: int, output: int) -> int:
        """Calibrate and return voltage to be applied to analog output.
        
        voltage: Voltage to be applied to the output.
        output: Output which should be switched
        """
        # Take a different set of calibration data depending on the output
        if output == 1:
            cal_ao = self.getCalibrationData(4)
        elif output == 2:
            cal_ao = self.getCalibrationData(5)
        # Calculate and return the value
        return self.calcCalibrate(voltage, cal_ao)

    
    def calibrateIn(self, value: int, input: int) -> int:
        """Convert value read at analog input to mV and return it.

        value: Value given for the file from the output
        input: Input at which the value was read
        """
        if input == 1:
            cal_ai = self.getCalibrationData(2)
        elif input == 2:
            cal_ai = self.getCalibrationData(3)

        # Return the calculated value 
        return self.calcCalibrate(value, cal_ai)
    
    def calibrateTemp(self, value: int, input: int) -> float:
        """Calibrate and return temperature read at PT input in °C.

        value: Value given for the file from the output
        input: Input at which the value was read
        """
        if input == 1:
            cal_Temp = self.getCalibrationData(0)
        elif input == 1:
            cal_Temp = self.getCalibrationData(1)
        
        # Return the calculated value in °C
        return (self.calcCalibrate(value, cal_Temp)-1000)/(3.91)

    def read_inputs(self) :
        """Read compact controller inputs."""
        print(self.input_data)
        # Fill database
        file_contents = {}
        for path, file in self._read_fds.items():
            file_content = file.read()
            file.seek(0)
            if file_content:
                file_contents[path] = file_content
            else:
                # Did not read correct value; use the old one for a cycle
                pass

        # create input image
        input_data = {}
        for ii, loc in self.file_map["pii"].items():
            if isinstance(loc, dict):
                data = {}
                for num, path in loc.items():
                    content = file_contents.get(path)
                    if content is not None:
                        data[num] = content
                # Update directly to preserve unchanged values
                self.input_data[self.item_num][ii].update(data)
            else:
                content = file_contents.get(loc)
                if content is not None:
                    input_data[ii] = content

        self.input_data[self.item_num].update(input_data)

    def write_outputs(self):
        """Write compact controller outputs from output image.
        
        Return all state variables that should be fed into the function the next time.
        Also set the input image to the new value to avoid reading every
        new cycle.
        """
        print(self.output_data)
        file_contents = {}
        for ii, content in self.output_data[self.item_num].items():
            if isinstance(content, dict):
                for num, value in content.items():
                    path = self.file_map["piq"][ii][num]
                    file_contents[path] = value
            else:
                path = self.file_map["piq"][ii]
                file_contents[path] = content
                # Take digital output value as input for next cycle
                self.input_data[self.item_num][ii] = value
        
        for path, value in file_contents.items():
            file = self._write_fds[path]
            file.write(value)
            file.seek(0)

    def reset(self) -> None:
        """Reset the output interfaces and close the file descriptors."""
        logger.info("Resetting outputs...")
        for f in self._write_fds.values():
            f.write("0")

        logger.debug("Closing file descriptors...")
        (file.close() for file in self._read_fds.values())
        (file.close() for file in self._write_fds.values())
