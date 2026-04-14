"""wagoplc.controller

This module holds the controller factory and I/O wrapper classes
for use by both the programmer and the library.

- Controller: the controller base class from which every controller version inherits
- IOHandler: handle the I/O wrapper classes and state variables for a task
- IO: base class for an I/O interface, child classes: DI, DO, AI, AO, PT, NI, DIO, AIO
"""
from typing import Any
import logging

from wagoplc.constants import LOG_FILE
from wagoplc.fb import TP

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=LOG_FILE,
    format="%(levelname)s - %(asctime)s - %(name)s: %(message)s",
    level=logging.DEBUG
)


class IO:
    """Generic I/O superclass to store interface id."""

    def __init__(self, id: int, module: str = ""):
        """Save interface and module numbers.

        id: interface number
        module: module number
        """
        if not isinstance(id, int):
            raise ValueError("Expected and integer id.")
        self.id = id
        self.module = module

    def __eq__(self, other):
        return isinstance(self, other.__class__) and self.id == other.id
    
    def __str__(self):
        return f"{type(self).__name__}({self.id})"

class DI(IO): 
    pass
class DO(IO): 
    pass
class AI(IO): 
    pass
class AO(IO): 
    pass
class NI(IO): 
    pass
class PT(IO): 
    pass
class DIO(IO):
    def __init__(self, id: int, type: int, module: str = ""):
        super().__init__(id, module)
        self.type = type
class AIO(DIO): 
    pass


class Controller:
    """The controller interface and basic functionality.
    
    Needs to be implemented by every PLC added to the library.
    Each I/O function takes a module parameter referring to the
    controller module. It is forwarded to the controller specific
    _get_data and _set_data functions.
    
    - digitalWrite: write the digital outputs
    - analogWrite: write the analog outputs
    - digitalRead: read the digital inputs
    - analogRead: read the analog inputs
    - tempRead: read the temperature inputs
    - calibrateIn, calibrateOut, calibrateTemp: calibrate analog values
    - read_inputs: read and store controller inputs
    - write_outputs: write stored values to controller outputs
    - reset: reset all controller outputs
    """

    def __init__(self):
        self.specs = {}

    # The following functions read from the input image
    # or write to the output image
    def digitalWrite(self, output: int, value: int, module: str) -> bool:
        """Switch the output to the specified value.

        output: Digital output to be switched
        value: Value which the selected output should be set to
        Return True if value is written, False if out does not exist.
        """
        # Read the current state to calculate the new value
        if (currentValue := self._get_data(DO, output, module)) is None:
            logger.warning(f"Digital output {output} for module {module} does not exist.")
            return False
        currentValue = int(currentValue)

        # Addition or rather subtraction to the current state to switch the corresponding output
        # Least Significant Bit corresponds to digital output 1, the 4th bit corresponds to output 4
        # A number from 0 to 15 is written to the file
        mask = (1 << (output - 1))
        if value:
            currentValue = currentValue | mask
        else:
            currentValue = currentValue & ~mask

        # Write the calculated value for the new configuration to the output image
        self._set_data(DO, output, module, str(currentValue))
        return True

    def analogWrite(self, output: int, voltage: int, module: str) -> bool:
        """Switch the output to the specified voltage.

        Return False if analog output does not exist,
        else return True.
        
        output: Analog output to be switched
        voltage: Voltage which the selected output should be set to
        """
        if self._get_data(AO, output, module) is None:
            logger.warning(f"Analog output {output} for module {module} does not exist.")
            return False

        if (voltage > 0 and voltage < 10001):
            voltage = self.calibrateOut(voltage, output)
        if voltage < 0:
            voltage = 0

        # Write the voltage, taken from the calibration for the corresponding output,
        # for the voltage to the file for the output
        # When turning off, zero is written to the file        
        self._set_data(AO, output, module, str(voltage))
        return True
        
    def digitalRead(self, input: int, module: str) -> int:
        """Read the specified digital input and return the value as boolean.

        input: Digital input to be read
        """
        if (value := self._get_data(DI, input, module)) is None:
            logger.warning(f"Digital input {input} for module {module} does not exist.")
            return False

        # Format the current state into a binary code
        value = int(value)
        num_inputs = self.specs[DI]
        binary_code = format(value, f"0{num_inputs}b")
        input_bit = num_inputs - input

        # Return the value of the state of the desired input
        # Note: last index (read from left to right) ist the Least Significant Bit.
        return int(binary_code[input_bit]) == 1
    
    def analogRead(self, input: int, module: str) -> int | bool:
        """Read analog input and return calibrated value in mV.

        Return False if the analog input does not exist.
        
        input: Analog input to be read
        """
        if (voltage := self._get_data(AI, input, module)) is None:
            logger.warning(f"Analog input {input} for module {module} does not exist.")
            return False
        return(self.calibrateIn(int(voltage), input))
    
    def tempRead(self, input: int, module: str) -> int:
        """Read PT input and return calibrated value in °C.

        Return False if the PT input does not exist.

        input: PT input to be read
        """
        if (voltage := self._get_data(PT, input, module)) is None:
            logger.warning(f"PT input {input} for module {module} does not exist.")
            return False

        # Calibrate the value and return it
        return(self.calibrateTemp(voltage, input))

    def _get_data(self, io: IO, input: int, module: str) -> int | bool | None:
        """Get raw input/output data data and return it.
    
        Return None if the specified input does not exist.
        """
        raise NotImplementedError

    def _set_data(self, iq: DO | AO, output: int, module: str, value: str) -> bool:
        """Set raw output data and return True.

        Return False if the specified output does not exist.
        """
        raise NotImplementedError

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
    """Handle the I/O wrapper classes.
    
    - get_input_image: get an input image (variables -> values) for a task cycle
    - process_output_image: process output variables of the cycle function and write outputs
    - update_timers: update state of running timers if the program was stopped for a while
    - read: read from a specific input interface
    - write: write to a specific output interface
    """

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

    def get_input_image(self) -> dict[str, Any]:
        self.plc_obj.read_inputs()
        input_image = {}
        self.input_vars = set(self.inputs.keys())
        for var, io in self.inputs.items():
            input_image[var] = self.read(io)
        input_image.update(self.state_vars)
        return input_image

    def process_output_image(self, output_image: dict[str, Any]) -> None:
        for var, value in output_image.items():
            if var in self.input_vars:
                raise ValueError(
                f"Variable '{var}' is an input.")

            if var in self.outputs:
                self.write(self.outputs[var], value)
            else:
                self.state_vars[var] = value
        self.plc_obj.write_outputs()

    def update_timers(self, stop_duration: int):
        """Update start time of timer fbs, as program execution was paused."""
        def update_timer(var):
            name, value = var
            if isinstance(value, TP):
                if value.start_time is not None:
                    value.start_time += stop_duration
            return name, value
        self.state_vars = dict(map(update_timer, self.state_vars.items()))
    
    def read(self, io: IO):
        if isinstance(io, DI):
            return self.plc_obj.digitalRead(io.id, io.module)
        elif isinstance(io, AI):
            return self.plc_obj.analogRead(io.id, io.module)
        elif isinstance(io, (NI, PT)):
            return self.plc_obj.tempRead(io.id, io.module)
    
    def write(self, io: IO, value: int | bool):
        if isinstance(io, DO):
            return self.plc_obj.digitalWrite(io.id, value, io.module)
        elif isinstance(io, AO):
            return self.plc_obj.analogWrite(io.id, value, io.module)
