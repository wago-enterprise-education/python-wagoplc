"""
This module holds standard function blocks that can be imported and 
used in a PLC program.

- CTU: up-counter
- CTD: down-counter
- CTUD: up- and down-counter
"""

class FB:
    """Generic superclass for a function block."""

    def __init__(self):
        """Configure any initial settings."""
        pass

    def __call__(self, *args, **kwds):
        """Do what needs to be done."""
        raise NotImplementedError


class CTU(FB):
    """An up-counter function block."""

    def __init__(self, pv: int = 0):
        """
        pv: when this limit is reached by cv, q is set to True (default 0)
        """
        self.cv = 0
        self.r = False
        self.cu = False
        self.q = False
        self.pv = pv
        self._pv_max = 32767

    def __call__(self, cu: bool | None = None, r: bool | None = None) -> None:
        """Count up if a rising edge for cu is registered.
        
        cu: counter impulse (default None)
        r: reset impulse (default None)
        """
        if r and not self.r:
            self.cv = 0
        elif cu and not self.cu and self.cv < self._pv_max:
            self.cv += 1

        if r is not None:
            self.r = r
        if cu is not None:
            self.cu = cu

        self.q = self.cv >= self.pv


class CTD(FB):
    """A down-counter function block."""

    def __init__(self, pv: int = 0):
        """
        pv: if a rising edge is registered for ld, cv is set to this value (default 0)
        """
        self.cv = 2
        self.ld = False
        self.cd = False
        self.q = False
        self.pv = pv
        self._pv_min = -32768

    def __call__(self, cd: bool | None = None, ld: bool | None = None) -> None:
        """Count down if a rising edge for cd is registered.
        
        cd: counter impulse (default None)
        ld: reset impulse (default None)
        """
        if ld and not self.ld:
            self.cv = self.pv
        elif cd and not self.cd and self.cv > self._pv_min:
            self.cv -= 1

        if ld is not None:
            self.ld = ld
        if cd is not None:
            self.cd = cd

        self.q = self.cv <= 0


class CTUD(FB):
    """An up- and down-counter function block."""

    def __init__(self, pv: int = 0):
        """
        pv: when this limit is reached by cv, q is set to True
        """
        self.cv = 0
        self.r = False
        self.ld = False
        self.cu = False
        self.cd = False
        self.qu = False
        self.qd = False
        self.pv = pv
        self._pv_max = 32767
        self._pv_min = -32768


    def __call__(
            self, cu: bool | None = None, r: bool | None = None,
            cd: bool | None = None, ld: bool | None = None) -> None:
        """Count up/down if a rising edge for cu/cd is registered.
        
        cu: up-counter impulse (default None)
        cd: down-counter impulse (default None)
        r: up-counter reset impulse (default None)
        ld: down-counter reset impulse (default None)
        """
        if r and not self.r:
            self.cv = 0
        elif cu and not self.cu and self.cv < self._pv_max:
            self.cv += 1
        elif ld and not self.ld:
            self.cv = self.pv
        elif cd and not self.cd and self.cv > self._pv_min:
            self.cv -= 1

        if r is not None:
            self.r = r
        if cu is not None:
            self.cu = cu
        if ld is not None:
            self.ld = ld
        if cd is not None:
            self.cd = cd

        self.qu = self.cv >= self.pv
        self.qd = self.cv <= 0