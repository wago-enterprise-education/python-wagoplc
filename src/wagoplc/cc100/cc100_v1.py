
from dataclasses import dataclass
from io import TextIOWrapper
import logging
import os
import time

logger = logging.getLogger(__name__)

@dataclass
class SYSTEM_PATHS:
    # data paths on CC100
    DOUT_DATA: str = "/sys/kernel/dout_drv/DOUT_DATA"
    OUT_VOLTAGE1_POWERDOWN: str = "/sys/bus/iio/devices/iio:device0/out_voltage1_powerdown"
    OUT_VOLTAGE2_POWERDOWN: str = "/sys/bus/iio/devices/iio:device1/out_voltage2_powerdown"
    OUT_VOLTAGE1_RAW: str = "/sys/bus/iio/devices/iio:device0/out_voltage1_raw"
    OUT_VOLTAGE2_RAW: str = "/sys/bus/iio/devices/iio:device1/out_voltage2_raw"
    DIN: str = "/sys/devices/platform/soc/44009000.spi/spi_master/spi0/spi0.0/din"
    IN_VOLTAGE3_RAW: str = "/sys/bus/iio/devices/iio:device3/in_voltage3_raw"
    IN_VOLTAGE0_RAW: str = "/sys/bus/iio/devices/iio:device3/in_voltage0_raw"
    IN_VOLTAGE13_RAW: str = "/sys/bus/iio/devices/iio:device2/in_voltage13_raw"
    IN_VOLTAGE1_RAW: str = "/sys/bus/iio/devices/iio:device2/in_voltage1_raw"
    CALIB_DATA: str = "/etc/calib"
    OS_VERSION: str = "/etc/os-release"
    SERIAL_PORT: str = "/dev/ttySTM1"

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
            self.CALIB_DATA,
            self.OS_VERSION
        )

class CC100_v1:

    def __init__(self):
        self.input_image: dict[str, str] = {}
        self.output_image: dict[str, str] = {}
        self.system_paths = SYSTEM_PATHS()

    def digitalWrite(self, output, value):
        """Switch the output to the specified value.

        output: Digital output to be switched
        value: Value which the selected output should be set to
        Return True if value is written, False if out does not exist.
        """
        # Read the current state to calculate the new value
        currentValue = int(self.input_image[self.system_paths.DOUT_DATA])

        # Addition or rather subtraction to the current state to switch the corresponding output
        # Least Significant Bit corresponds to digital output 1, the 4th bit corresponds to output 4
        # A number from 0 to 15 is written to the file
        if output in range(1, 5):
            mask = (1 << (output - 1))
            if value:
                currentValue = currentValue | mask
            else:
                currentValue = currentValue & ~mask
        else:
            logger.warning("Digital output does not exist")
            return False

        # Write the calculated value for the new configuration to the output image
        self.output_image[self.system_paths.DOUT_DATA] = str(currentValue)

    def analogWrite(self, output, voltage):
        """Switch the output to the specified voltage.

        Return False if analog output does not exist,
        else return True.
        
        output: Analog output to be switched
        voltage: Voltage which the selected output should be set to
        """
        if output == 1:
            self.output_image[self.system_paths.OUT_VOLTAGE1_POWERDOWN] = "0"

            output_file = self.system_paths.OUT_VOLTAGE1_RAW
        elif output == 2:
            self.output_image[self.system_paths.OUT_VOLTAGE2_POWERDOWN] = "0"

            output_file = self.system_paths.OUT_VOLTAGE2_RAW
        else:
            logger.warning("Analog output does not exist")
            return False

        if (voltage > 0 and voltage < 10001):
            voltage = self.calibrateOut(voltage, output)
        if voltage < 0:
            voltage = 0

        # Write the voltage, taken from the calibration for the corresponding output,
        # for the voltage to the file for the output
        # When turning off, zero is written to the file
        self.output_image[output_file] = voltage
        
    def digitalRead(self, input):
        """Read the specified digital input and return the value as boolean.

        input: Digital input to be read
        """
        if input not in range(1,9):
            logger.warning("Digital input does not exist")
            return False
        
        # Read the state of the digital inputs on the CC100
        value = self.input_image[self.system_paths.DIN]

        # Format the current state into an 8-digit binary code
        value = int(value)
        value0B = format(value, "08b")

        # Calculate the position of the bit from the desired input
        inputBit = 8 - input

        # Return the value of the state of the desired input
        # Note: Last index(read from left to right) ist the Least Significant Bit.
        return int(value0B[inputBit]) == 1
        
    
    def digitalReadWait(self,input, value):
        """Read specified input until desired state is reached, then return True.

        Return False if digital input does not exist.

        input: Digital input to be checked
        value: State to be queried at the input
        """
        if input not in range(1,9):
            logger.warning("Digital input does not exist")
            return False
        
        value = int(value)

        # Check the input as long as it reaches the given state
        # Then end the loop and return True
        while True:
            if self.digitalRead(input) == value:
                break
        return True
    
    def analogRead(self, input):
        """Read analog input and return calibrated value in mV.

        Return False if analog input does not exist.

        input: Analog input to be read
        """
        # Read the state of the analog input on the CC100
        if input == 1:
            path=self.IN_VOLTAGE3_RAW
        elif input == 2:
            path=self.IN_VOLTAGE0_RAW
        else:
            logger.warning("Analog input does not exist")
            return False
        
        voltage = int(self.input_image[path])

        return(self.calibrateIn(voltage, input))
    
    def delay(iTime):
        iTime = iTime/1000
        time.sleep(iTime)

    def tempRead(self,input):
        """Read PT input and return calibrated value in °C.

        input: PT input to be read
        """
        if input == "PT1":
            path=self.IN_VOLTAGE13_RAW
        elif input == "PT2":
            path=self.IN_VOLTAGE1_RAW
        
        voltage = self.input_image[path]

        # Calibrate the value and returns it
        return(self.calibrateTemp(voltage, input))
    
    def serialReadLine(self):
        """Read incoming message on RS485 Port till eol and return data."""
        data = ""
        with open(self.SERIAL_PORT) as ser:
            data = ser.readline()
        return data
        
    def serialReadBytes(self,n):
        """Read a specified number of bytes in RS485 port and return data.

        n: number of bytes to read
        """
        data = ""
        with open(self.SERIAL_PORT, "r") as ser:
            data = ser.read(n)
        return data

    def serialWrite(self,message):
        """Write message to RS485 serial interface and return number of written bytes.

        message: String to write
        """
        written = -1
        with open(self.SERIAL_PORT, "w") as ser:
            written = ser.write(message)
        return written

    # Output calibration from: https://github.com/WAGO/cc100-howtos/blob/main/HowTo_Access_Onboard_IO/accessIO_CC100.py
    
    def readCalibrationData(self):
        """Read out calibration data from the CC100 and save it in global variable calib_data."""
        global calib_data
        calib_data = self.input_image[self.system_paths.CALIB_DATA]

    def getCalibrationData(value):
        """Return the calibration data for the required row of the table.

        value: the row to read
        """
        return calib_data[value].rstrip().split(' ', 4)

    def calcCalibrate(val_uncal, calib):
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
    
    def calibrateOut(self,voltage, output):
        """Calibrate and return voltage to be applied to analog output.
        
        voltage: Voltage to be applied to the output.
        output: Output which should be switched
        """
        self.readCalibrationData()
        # Take a different set of calibration data depending on the output
        if output == 1:
            cal_ao = self.getCalibrationData(4)
        elif output == 2:
            cal_ao = self.getCalibrationData(5)
        # Calculate and return the value
        return self.calcCalibrate(voltage, cal_ao)

    
    def calibrateIn(self,value, input):
        """Convert value read at analog input to mV and return it.

        value: Value given for the file from the output
        input: Input at which the value was read
        """
        self.readCalibrationData()
        if input == 1:
            cal_ai = self.getCalibrationData(2)
        if input == 2:
            cal_ai = self.getCalibrationData(3)
        #Return the calculated value 
        return self.calcCalibrate(value, cal_ai)
    
    
    def calibrateTemp(self,value, input):
        """Calibrate and return temperature read at PT input in °C.

        value: Value given for the file from the output
        input: Input at which the value was read
        """
        self.readCalibrationData()
        if input == "PT1":
            cal_Temp = self.getCalibrationData(0)
        if input == "PT2":
            cal_Temp = self.getCalibrationData(1)
        #Return the calculated value in °C
        return (self.calcCalibrate(value, cal_Temp)-1000)/(3.91)

    def read_inputs(self, file_descriptors: dict[str, TextIOWrapper]):
        """Read compact controller inputs and write input image."""
        for path, file in file_descriptors.items():
            self.input_image[path] = file.read()
            file.seek(0)

    def write_outputs(self, file_descriptors: dict[str, TextIOWrapper]):
        """Write compact controller outputs from output image.
        
        Also set the input image to the new value to avoid reading every
        new cycle.
        """
        for path, value in self.output_image.items():
            file = file_descriptors[path]
            file.write(value)
            file.seek(0)
            self.input_image[path] = value
        