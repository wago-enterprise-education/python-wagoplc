import logging
import os

from wagoplc.controller import Controller, IO, DI, DO, AI, AO, PT

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
        self.file_map = {
            DI: self.DIN,
            AI: {
                1: self.IN_VOLTAGE3_RAW, 2: self.IN_VOLTAGE0_RAW
            },
            PT: {
                1: self.IN_VOLTAGE13_RAW, 2: self.IN_VOLTAGE1_RAW
            },
            DO: self.DOUT_DATA,
            AO: {
                1: self.OUT_VOLTAGE1_RAW, 2: self.OUT_VOLTAGE2_RAW,
            }
        }
        self.specs = {
            DI: 8,
            AI: 2,
            PT: 2,
            DO: 4,
            AO: 2
        }

        self.input_data: dict[str, str] = {}
        self.output_data: dict[str, str] = {}

    def get_write_paths(self) -> tuple[str]:
        return (
            self.DOUT_DATA,
            self.SERIAL_PORT,
            self.OUT_VOLTAGE1_POWERDOWN,
            self.OUT_VOLTAGE2_POWERDOWN,
            self.OUT_VOLTAGE1_RAW,
            self.OUT_VOLTAGE2_RAW
        )

    def get_read_paths(self) -> tuple[str]:
        return (
            self.DIN,
            self.IN_VOLTAGE0_RAW,
            self.IN_VOLTAGE3_RAW,
            self.IN_VOLTAGE13_RAW,
            self.IN_VOLTAGE1_RAW,
        )

    def get_read_once_paths(self) -> tuple[str]:
        return (
            self.CALIB_DATA,
            self.DOUT_DATA
        )

    def init_fds(self):
        """Get system file descriptors for the CC100 v1."""
        self._read_fds = {path: open(TEST_DATA + path, "r") for path in self.get_read_paths()}
        # Read digital output file initially and add it to the input image.
        # The value is updated after every write, the file is kept open
        # in write mode.  Otherwise, it would be necessary to use update file mode
        # (r+), which is too costly.
        for path in self.get_read_once_paths():
            with open(TEST_DATA + path, "r") as f:
                self.input_data[path] = f.read()
        self._write_fds = {path: open(TEST_DATA + path, "w") for path in self.get_write_paths()}

    def analogWrite(self, output: int, voltage: int, module: str) -> bool:
        """Switch the output to the specified voltage.

        Return False if analog output does not exist,
        else return True.
        
        output: Analog output to be switched
        voltage: Voltage which the selected output should be set to
        """
        if output == 1:
            self.output_data[self.OUT_VOLTAGE1_POWERDOWN] = "0"
        elif output == 2:
            self.output_data[self.OUT_VOLTAGE2_POWERDOWN] = "0"
        super().analogWrite(output, voltage, module)

    # Output calibration from: https://github.com/WAGO/cc100-howtos/blob/main/HowTo_Access_Onboard_IO/accessIO_CC100.py
    def getCalibrationData(self, value: int) -> list[str]:
        """Return the calibration data for the required row of the table.

        value: the row to read
        """
        calib_data = self.input_data[self.CALIB_DATA].strip().split("\n")[1:]
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

    def _get_data(self, io: IO, input: int, module: str) -> int | bool | None:
        if input not in range(1, self.specs[io]):
            return None
        path = self.file_map[io]
        if isinstance(path, dict):
            path = path[input]
        return self.input_data[path]

    def _set_data(self, iq: DO | AO, output: int, module: str, value: str) -> bool:
        if output not in range(1, self.specs[iq]):
            return False
        path = self.file_map[iq]
        if isinstance(path, dict):
            path = path[output]
        self.output_data[path] = value

    def read_inputs(self) :
        """Read compact controller inputs."""
        print(self.input_data)
        # Fill database
        for path, file in self._read_fds.items():
            file_content = file.read()
            file.seek(0)
            if file_content:
                self.input_data[path] = file_content
            else:
                # Did not read correct value; use the old one for a cycle
                pass

    def write_outputs(self):
        """Write compact controller outputs from output image.
        
        Return all state variables that should be fed into the function the next time.
        Also set the input image to the new value to avoid reading every
        new cycle.
        """
        print(self.output_data)
        for path, value in self.output_data.items():
            file = self._write_fds[path]
            file.write(value)
            file.seek(0)
            self.input_data[path] = value

    def reset(self) -> None:
        """Reset the output interfaces and close the file descriptors."""
        logger.info("Resetting outputs...")
        for f in self._write_fds.values():
            f.write("0")

        logger.debug("Closing file descriptors...")
        (file.close() for file in self._read_fds.values())
        (file.close() for file in self._write_fds.values())
