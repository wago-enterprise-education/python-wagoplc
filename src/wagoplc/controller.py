"""wagoplc.controller

This module holds the controller factory and I/O wrapper classes
for use by both the programmer and the library.
"""

from typing import Any

class Controller:
    """The controller interface and basic functionality.
    
    Needs to be implemented by every PLC added to the library.
    """

    def __init__(self):
        self.input_data: dict[str, str] = {}
        self.output_data: dict[str, str] = {}

    # The following functions read from the input image
    # or write to the output image
    def digitalWrite(self, output: int, value: int, module: str) -> bool:
        """Switch the output to the specified value.

        output: Digital output to be switched
        value: Value which the selected output should be set to
        Return True if value is written, False if out does not exist.
        """
        if output not in range(1, self.input_data[module]["specs"][DI]):
            return False

        # Read the current state to calculate the new value
        currentValue = int(self.input_data[module][DO])

        # Addition or rather subtraction to the current state to switch the corresponding output
        # Least Significant Bit corresponds to digital output 1, the 4th bit corresponds to output 4
        # A number from 0 to 15 is written to the file
        mask = (1 << (output - 1))
        if value:
            currentValue = currentValue | mask
        else:
            currentValue = currentValue & ~mask

        # Write the calculated value for the new configuration to the output image
        self.output_data[module][DO] = str(currentValue)
        return True

    def analogWrite(self, output: int, voltage: int, module: str) -> bool:
        """Switch the output to the specified voltage.

        Return False if analog output does not exist,
        else return True.
        
        output: Analog output to be switched
        voltage: Voltage which the selected output should be set to
        """
        if output not in range(1, self.input_data[module]["specs"][AO]):
            return False

        if (voltage > 0 and voltage < 10001):
            voltage = self.calibrateOut(voltage, output)
        if voltage < 0:
            voltage = 0

        # Write the voltage, taken from the calibration for the corresponding output,
        # for the voltage to the file for the output
        # When turning off, zero is written to the file        
        self.output_data[module][AO][output] = str(voltage)
        return True
        
    def digitalRead(self, input: int, module: str) -> int:
        """Read the specified digital input and return the value as boolean.

        input: Digital input to be read
        """
        value = self.input_data[module][DI]
        num_inputs = self.input_data[module]["specs"][DI]

        # Format the current state into a binary code
        value = int(value)
        binary_code = format(value, f"0{num_inputs}b")

        # Calculate the position of the bit from the desired input
        input_bit = num_inputs - input

        # Return the value of the state of the desired input
        # Note: last index (read from left to right) ist the Least Significant Bit.
        return int(binary_code[input_bit]) == 1
    
    def analogRead(self, input: int, module: str) -> int|bool:
        """Read analog input and return calibrated value in mV.

        Return False if the analog input does not exist.
        
        input: Analog input to be read
        """
        if input not in range(1, self.input_data[module]["specs"][AI]):
            return False
        voltage = int(self.input_data[module][AI][input])

        return(self.calibrateIn(voltage, input))
    
    def tempRead(self, input: int, module: str) -> int:
        """Read PT input and return calibrated value in °C.

        Return False if the PT input does not exist.

        input: PT input to be read
        """
        if input not in range(1, self.input_data[module]["specs"][PT]):
            return False
        voltage = self.input_data[module][PT][input]

        # Calibrate the value and return it
        return(self.calibrateTemp(voltage, input))
    
    def calibrateIn(self):
        raise NotImplementedError
    
    def calibrateOut(self):
        raise NotImplementedError
    
    def calibrateTemp(self):
        raise NotImplementedError
    
    def read_inputs():
        """Fill the input image with actual data."""
        raise NotImplementedError
    
    def write_outputs():
        """Actually write the outputs from the output image."""
        raise NotImplementedError
    
    def reset():
        """Reset outputs and close any file descriptors."""
        raise NotImplementedError


class IOHandler:
    """Handle the I/O wrapper classes."""

    def __init__(self, plc_object: Controller, input_mapping: dict[str, Any], var_mapping: dict[str, Any]):
        self.plc_obj = plc_object

        self.inputs = dict(
            filter(
                lambda map: isinstance(map[1], (DI, AI, PT, NI)), 
                input_mapping.items()
            )
        )
        self.outputs = dict(
            filter(
                lambda map: isinstance(map[1], (DO, AO)), 
                var_mapping.items()
            )
        )

        self.state_vars = dict(filter(
            lambda p: p[0] not in {**self.inputs, **self.outputs}, input_mapping.items()
        ))

    def get_input_image(self) -> None:
        self.plc_obj.read_inputs()
        input_image = {}
        for var, io in self.inputs.items():
                input_image[var] = self.read(io)
        input_image.update(self.state_vars)
        return input_image

    def process_output_image(self, output_image: dict[str, Any]) -> None:
        for var, value in output_image.items():
            if var in self.outputs:
                self.write(self.outputs[var], value)
            else:
                self.state_vars[var] = value
        self.plc_obj.write_outputs()
    
    def read(self, io: IO):
        module = io.module or self.plc_obj.item_num
        if isinstance(io, DI):
            return self.plc_obj.digitalRead(io.id, module)
        elif isinstance(io, AI):
            return self.plc_obj.analogRead(io.id, module)
        elif isinstance(io, (NI, PT)):
            return self.plc_obj.tempRead(io.id, module)
    
    def write(self, io: IO, value: int | bool):
        module = io.module or self.plc_obj.item_num
        if isinstance(io, DO):
            return self.plc_obj.digitalWrite(io.id, value, module)
        elif isinstance(io, AO):
            return self.plc_obj.analogWrite(io.id, value, module)

class IO:
    """Generic I/O superclass to store interface id."""
    def __init__(self, id: int, module: str = ""):
        if not isinstance(id, int):
            raise ValueError("Expected and integer id.")
        self.id = id
        self.module = module

    def __eq__(self, other):
        return isinstance(self, other.__class__) and self.id == other.id
    
    def __str__(self):
        return f"{type(self).__name__}({self.id})"

class DI(IO): pass
class DO(IO): pass
class AI(IO): pass
class AO(IO): pass
class NI(IO): pass
class PT(IO): pass
class DIO(IO):
    def __init__(self, id: int, type: int, module: str = ""):
        super().__init__(id, module)
        self.type = type
class AIO(DIO): pass