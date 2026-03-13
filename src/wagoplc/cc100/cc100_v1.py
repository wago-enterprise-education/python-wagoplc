from io import TextIOWrapper
from typing import Any

import logging

from wagoplc.fb import FB

logger = logging.getLogger(__name__)

class IO:
    """Generic I/O superclass to store interface id."""
    def __init__(self, id: int):
        if not isinstance(id, int):
            raise ValueError("Expected and integer id.")
        self.id = id

    def __eq__(self, other):
        return isinstance(self, other.__class__) and self.id == other.id
    
    def __str__(self):
        return f"{type(self).__name__}({self.id})"


class DI(IO):
    def read(self, cc_obj) -> bool:
        return cc_obj.digitalRead(self.id)


class DO(IO):
    def write(self, cc_obj, value) -> bool:
        return cc_obj.digitalWrite(self.id, value)


class AI(IO):
    def read(self, cc_obj) -> int:
        return cc_obj.analogRead(self.id)


class AO(IO):
    def write(self, cc_obj, value: int) -> bool:
        return cc_obj.analogWrite(self.id, value)


class IOError(Exception):
    pass


class CC100_v1:
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
        self.input_image: dict[str, str] = {}
        self.output_image: dict[str, str] = {}

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

    def digitalWrite(self, output: int, value: int) -> bool:
        """Switch the output to the specified value.

        output: Digital output to be switched
        value: Value which the selected output should be set to
        Return True if value is written, False if out does not exist.
        """
        # Read the current state to calculate the new value
        currentValue = int(self.input_image[self.DOUT_DATA])

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
        self.output_image[self.DOUT_DATA] = str(currentValue)
        return True

    def analogWrite(self, output: int, voltage: int) -> bool:
        """Switch the output to the specified voltage.

        Return False if analog output does not exist,
        else return True.
        
        output: Analog output to be switched
        voltage: Voltage which the selected output should be set to
        """
        if output == 1:
            self.output_image[self.OUT_VOLTAGE1_POWERDOWN] = "0"

            output_file = self.OUT_VOLTAGE1_RAW
        elif output == 2:
            self.output_image[self.OUT_VOLTAGE2_POWERDOWN] = "0"

            output_file = self.OUT_VOLTAGE2_RAW
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
        self.output_image[output_file] = str(voltage)
        return True
        
    def digitalRead(self, input: int)-> int:
        """Read the specified digital input and return the value as boolean.

        input: Digital input to be read
        """
        if input not in range(1,9):
            logger.warning("Digital input does not exist")
            return False
        
        # Read the state of the digital inputs on the CC100
        value = self.input_image[self.DIN]

        # Format the current state into an 8-digit binary code
        value = int(value)
        value0B = format(value, "08b")

        # Calculate the position of the bit from the desired input
        inputBit = 8 - input

        # Return the value of the state of the desired input
        # Note: Last index(read from left to right) ist the Least Significant Bit.
        return int(value0B[inputBit]) == 1
        
    
    def digitalReadWait(self, input: int, value: int)-> bool:
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
    
    def analogRead(self, input: int)-> int|bool:
        """Read analog input and return calibrated value in mV.

        Return False if analog input does not exist.

        input: Analog input to be read
        """
        # Read the state of the analog input on the CC100
        if input == 1:
            path = self.IN_VOLTAGE3_RAW
        elif input == 2:
            path = self.IN_VOLTAGE0_RAW
        else:
            logger.warning("Analog input does not exist")
            return False
        
        voltage = int(self.input_image[path])

        return(self.calibrateIn(voltage, input))

    def tempRead(self, input: int)-> int:
        """Read PT input and return calibrated value in °C.

        input: PT input to be read
        """
        if input == "PT1":
            path = self.IN_VOLTAGE13_RAW
        elif input == "PT2":
            path = self.IN_VOLTAGE1_RAW
        
        voltage = self.input_image[path]

        # Calibrate the value and returns it
        return(self.calibrateTemp(voltage, input))
    
    def serialReadLine(self)-> str:
        """Read incoming message on RS485 Port till eol and return data."""
        data = ""
        with open(self.SERIAL_PORT) as ser:
            data = ser.readline()
        return data
        
    def serialReadBytes(self,n: int)-> str:
        """Read a specified number of bytes in RS485 port and return data.

        n: number of bytes to read
        """
        data = ""
        with open(self.SERIAL_PORT, "r") as ser:
            data = ser.read(n)
        return data

    def serialWrite(self,message: str)-> int:
        """Write message to RS485 serial interface and return number of written bytes.

        message: String to write
        """
        written = -1
        with open(self.SERIAL_PORT, "w") as ser:
            written = ser.write(message)
        return written

    # Output calibration from: https://github.com/WAGO/cc100-howtos/blob/main/HowTo_Access_Onboard_IO/accessIO_CC100.py
    def getCalibrationData(self, value: int)-> list[str]:
        """Return the calibration data for the required row of the table.

        value: the row to read
        """
        calib_data = self.input_image[self.CALIB_DATA].strip().split("\n")[1:]
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
    
    def calibrateOut(self, voltage: int, output: int)-> int:
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

    
    def calibrateIn(self,value: int, input: int)-> int:
        """Convert value read at analog input to mV and return it.

        value: Value given for the file from the output
        input: Input at which the value was read
        """
        if input == 1:
            cal_ai = self.getCalibrationData(2)
        if input == 2:
            cal_ai = self.getCalibrationData(3)
        #Return the calculated value 
        return self.calcCalibrate(value, cal_ai)
    
    
    def calibrateTemp(self, value: int, input: int)-> float:
        """Calibrate and return temperature read at PT input in °C.

        value: Value given for the file from the output
        input: Input at which the value was read
        """
        if input == "PT1":
            cal_Temp = self.getCalibrationData(0)
        if input == "PT2":
            cal_Temp = self.getCalibrationData(1)
        #Return the calculated value in °C
        return (self.calcCalibrate(value, cal_Temp)-1000)/(3.91)

    def read_inputs(self, fds: dict[str, TextIOWrapper],
                    input_mapping: dict[str, Any] = {}) -> dict[str, bool | int | str]:
        """Read compact controller inputs and write input image.
        
        fds: read system file descriptors
        input_mapping: variables mapped to input interface objects
        """
        input_image = {}
        # Fill database
        for path, file in fds.items():
            file_content = file.read()
            file.seek(0)
            if file_content:
                self.input_image[path] = file_content
            else:
                # Did not read correct value; use the old one for a cycle
                pass

        if not input_mapping:
            return {}
        
        # Map variables to values
        for var, value in input_mapping.items():
            if isinstance(value, IO):
                # Read the inputs and add them to the image
                input_image[var] = value.read(self)
            else:
                # Write any other variable (e. g. a function block) unchanged
                # into the image
                input_image[var] = value
        return input_image

    def write_outputs(self, fds: dict[str, TextIOWrapper],
                      output_image: dict[str, bool | int | str] = {},
                      outputs: dict[str, Any] = {}) -> dict[str, Any]:
        """Write compact controller outputs from output image.
        
        Return all state variables that should be fed into the function the next time.
        Also set the input image to the new value to avoid reading every
        new cycle.

        fds: write system file descriptors
        output_image: output variables from the cycle function
        outputs: variables mapped to output interfaces
        """
        retain_vars = {}
        for var, value in output_image.items():
            if var in outputs:
                outputs[var].write(self, value)
            else:
                retain_vars[var] = value

        for path, value in self.output_image.items():
            file = fds[path]
            file.write(value)
            file.seek(0)
            self.input_image[path] = value

        return retain_vars

    def reset_outputs(self, fds: dict[str, TextIOWrapper]) -> None:
        """Reset the output interfaces to null.
        
        fds: write system file descriptors
        """
        for path in self.output_image:
            self.output_image[path] = "0"
        self.write_outputs(fds)
