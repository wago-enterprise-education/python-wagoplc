
import logging
import os
import time

logger = logging.getLogger(__name__)

class CC100_v1:
    # data paths on CC100
    DOUT_DATA = "/sys/kernel/dout_drv/DOUT_DATA"
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
    OS_VERSION = "/etc/os-release"
    SERIAL_PORT = "/dev/ttySTM1"

    def __init__(self):
        pass

    @classmethod
    def get_path(cls):
        return cls.DOUT_DATA
    
    @classmethod
    def digitalWrite(cls,output, value):
        """Switch the output to the specified value.

        output: Digital output to be switched
        value: Value which the selected output should be set to
        Return True if value is written, False if out does not exist.
        """
        # Read the current state to calculate the new value in the file
        file = open(cls.DOUT_DATA, "r")
        currentValue = int(file.read())
        file.close()

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

        # Writes the calculated value for the new configuration to the file on the CC100
        file = open(cls.DOUT_DATA, "w")
        file.write(str(currentValue))
        file.close()

        return True

    @classmethod
    def analogWrite(cls,output, voltage):
        """Switch the output to the specified voltage.

            Return False if analog outpout does not exist,
            else return True.

        output: Analog output to be switched
        voltage: Voltage which the selected output should be set to
        """
        if output == 1:
            file = open(cls.OUT_VOLTAGE1_RAW, "w")
            file.write(str(voltage))
            file.close()

        elif output == 2:
            file=open(cls.OUT_VOLTAGE2_RAW, "w")
            file.write(str(voltage))
            file.close()

        else: 
            logger.warning("Output does not exist")    
            return False

        if (voltage>0 and voltage <10001):
            voltage = cls.calibrateOut(voltage, output)
        if voltage < 0:
            voltage = 0

        # Activate the analog outputs on the CC100
        file = open(cls.OUT_VOLTAGE1_POWERDOWN, "w")
        file.write("0")
        file.close()

        file = open(cls.OUT_VOLTAGE2_POWERDOWN, "w")
        file.write("0")
        file.close()

        # Write the voltage, taken from the calibration for the corresponding output,
        # for the voltage to the file for the output
        # When turning off, zero is written to the file

        return True

    @classmethod
    def digitalRead(cls,input):
        """Read the specified digital input and return the value as boolean.

        input: Digital input to be read
        """
        if input not in range(1,9):
            logger.warning("Digital input does not exist")
        # Read the state of the digital inputs on the CC100
        file = open (cls.DIN, "r")
        value = file.readline()
        file.close()

        # Format the current state into an 8-digit binary code
        value = int(value)
        value0B = format(value, "08b")

        # Calculate the position of the bit from the desired input
        inputBit = 8 - input

        # Return the value of the state of the desired input
        # Note: Last index(read from left to right) ist the Least Significant Bit.
        if int(value0B[inputBit]) == 1:
            return True
        else:
            return False
        
    @classmethod
    def digitalReadWait(cls,input, value):
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
            if cls.digitalRead(input) == value:
                break
        return True
    
    @classmethod
    def analogRead(cls,input):
        """Read analog input and return calibrated value in mV.

        Return False if analog input does not exist.

        input: Analog input to be read
        """

        # Read the state of the analog input on the CC100
        if input == 1:
            path=cls.IN_VOLTAGE3_RAW
        elif input == 2:
            path=cls.IN_VOLTAGE0_RAW
        else:
            logger.warning("Analog input does not exist")
            return False
        
        file = open(path, "r")
        voltage = int(file.readline())
        file.close()

        return(cls.calibrateIn(voltage, input))
    
    @classmethod
    def delay(iTime):
        iTime = iTime/1000
        time.sleep(iTime)

    @classmethod
    def tempRead(cls,input):
        """Read PT input and return calibrated value in °C.

        input: PT input to be read
        """
        
        if input == "PT1":
            path=cls.IN_VOLTAGE13_RAW
        elif input == "PT2":
            path=cls.IN_VOLTAGE1_RAW
        
        file = open(path, "r")
        voltage = int(file.readline())
        file.close()

        # Calibrate the value and returns it
        return(cls.calibrateTemp(voltage, input))
    @classmethod
    def serialReadLine(cls):
        """Read incoming message on RS485 Port till eol and return data."""
        data = ""
        with open(cls.SERIAL_PORT) as ser:
            data = ser.readline()
        return data
        
    @classmethod
    def serialReadBytes(cls,n):
        """Read a specified number of bytes in RS485 port and return data.

        n: number of bytes to read
        """
        data = ""
        with open(cls.SERIAL_PORT, "r") as ser:
            data = ser.read(n)
        return data

    @classmethod
    def serialWrite(cls,message):
        """Write message to RS485 serial interface and return number of written bytes.

        message: String to write
        """
        written = -1
        with open(cls.SERIAL_PORT, "w") as ser:
            written = ser.write(message)
        return written


    # Output calibration from: https://github.com/WAGO/cc100-howtos/blob/main/HowTo_Access_Onboard_IO/accessIO_CC100.py
    @classmethod
    def readCalibrationData(cls):
        """Read out calibration data from the CC100 and save it in global variable calib_data."""
        global calib_data
        file = open(cls.CALIB_DATA, "r")
        calib_data = file.readlines()[1:]    
        file.close()

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

    @classmethod
    def calibrateOut(cls,voltage, output):
        """Calibrate and return voltage to be applied to analog output.
        
        voltage: Voltage to be applied to the output.
        output: Output which should be switched
        """
        
        cls.readCalibrationData()
        # Take a different set of calibration data depending on the output
        if output == 1:
            cal_ao = cls.getCalibrationData(4)
        elif output == 2:
            cal_ao = cls.getCalibrationData(5)
        # Calculate and return the value
        return cls.calcCalibrate(voltage, cal_ao)

    @classmethod
    def calibrateIn(cls,value, input):
        """Convert value read at analog input to mV and return it.

        value: Value given for the file from the output
        input: Input at which the value was read
        """
        cls.readCalibrationData()
        if input == 1:
            cal_ai = cls.getCalibrationData(2)
        if input == 2:
            cal_ai = cls.getCalibrationData(3)
        #Return the calculated value 
        return cls.calcCalibrate(value, cal_ai)
    
    @classmethod
    def calibrateTemp(cls,value, input):
        """Calibrate and return temperature read at PT input in °C.

        value: Value given for the file from the output
        input: Input at which the value was read
        """
        cls.readCalibrationData()
        if input == "PT1":
            cal_Temp = cls.getCalibrationData(0)
        if input == "PT2":
            cal_Temp = cls.getCalibrationData(1)
        #Return the calculated value in °C
        return (cls.calcCalibrate(value, cal_Temp)-1000)/(3.91)
        