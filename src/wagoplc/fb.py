"""
This module holds standard function blocks that can be imported and 
used in a PLC program.

- CTU: up-counter
"""

class FB:
    """Generic superclass for a function block."""

    def __init__(self):
        pass

    def __call__(self, *args, **kwds):
        """Do what needs to be done."""
        raise NotImplementedError


class CTU(FB):
    """An up-counter function block."""

    def __init__(self, pv: int):
        self.cv = 0
        self.q = False
        self.pv = pv
        self._risingEdge = True

    def __call__(self, cu: bool) -> bool:
        """Count up if a rising edge is registered.
        
        Return whether it was counted up.
        """
        if cu and self._risingEdge:
            self.cv += 1
            self._risingEdge = False
        elif not cu:
            self._risingEdge = True

        if self.cv == self.pv:
            self.q = True
        elif self.cv < self.pv and self.q:
            self.q = False
        return cu

    def reset(self) -> None:
        """Reset the count value to zero."""
        self.cv = 0