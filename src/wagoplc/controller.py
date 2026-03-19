"""wagoplc.controller

This module holds the controller factory and I/O wrapper classes
for use by both the programmer and the library.
"""

from typing import Any

class Controller:
    """The controller interface.
    
    Needs to be implemented by every PLC added to the library.
    """

    def __init__(self):
        self.input_image: dict[str, str] = {}
        self.output_image: dict[str, str] = {}

    # The following functions read from the input image
    # or write to the output image
    def digitalRead(self, input: int):
        raise NotImplementedError
    
    def analogRead(self, input: int):
        raise NotImplementedError
    
    def digitalWrite(self, output: int, value: int):
        raise NotImplementedError
    
    def analogWrite(self, output: int, value: int):
        raise NotImplementedError
    
    def tempRead(self, input: int):
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
        if isinstance(io, DI):
            return self.plc_obj.digitalRead(io.id)
        elif isinstance(io, AI):
            return self.plc_obj.analogRead()
        elif isinstance(io, (NI, PT)):
            return self.plc_obj.tempRead(io.id)
    
    def write(self, io: IO, value: int | bool):
        if isinstance(io, DO):
            return self.plc_obj.digitalWrite(io.id, value)
        elif isinstance(io, AO):
            return self.plc_obj.analogWrite(io.id, value)

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

class DI(IO): pass
class DO(IO): pass
class AI(IO): pass
class AO(IO): pass
class NI(IO): pass
class PT(IO): pass
