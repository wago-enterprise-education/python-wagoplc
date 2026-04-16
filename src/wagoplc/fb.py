"""Standard library.
This module holds function blocks defined by the PLC programming
norm DIN EN 61131-3. They can be imported and used in a PLC program.

- CTU: up-counter
- CTD: down-counter
- CTUD: up- and down-counter
- TP: impulse giver
- TON: switch-on-timer
- TOF: switch-off-timer
- RS: RS latch
- SR: SR latch
- R_TRIG: trigger on rising flank
- F_TRIG: trigger on falling flank
"""

import time

def _rising_edge(signal: bool, last_signal: bool):
    """Return whether the signal is a rising edge."""
    return signal and not last_signal

def _falling_edge(signal: bool, last_signal: bool):
    """Return whether the signal is a falling edge."""
    return not signal and last_signal


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

    def __call__(self, cu: bool = False, r: bool = False, pv: int = 0) -> None:
        """Count up if a rising edge for cu is registered.
        
        cu: counter impulse (default False)
        r: reset impulse (default False)
        """
        if _rising_edge(r, self.r):
            self.cv = 0
        elif _rising_edge(cu, self.cu) and self.cv < self._pv_max:
            self.cv += 1

        self.r = r
        self.cu = cu
        self.pv = pv or self.pv

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

    def __call__(self, cd: bool = False, ld: bool = False) -> None:
        """Count down if a rising edge for cd is registered.
        
        cd: counter impulse (default False)
        ld: reset impulse (default False)
        """
        if _rising_edge(ld, self.ld):
            self.cv = self.pv
        elif _rising_edge(cd, self.cd) and self.cv > self._pv_min:
            self.cv -= 1

        self.ld = ld
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
            self, cu: bool = False, r: bool = False,
            cd: bool = False, ld: bool = False, pv: int = 0) -> None:
        """Count up/down if a rising edge for cu/cd is registered.
        
        cu: up-counter signal (default False)
        cd: down-counter signal (default False)
        r: up-counter reset signal (default False)
        ld: down-counter reset signal (default False)
        """
        if _rising_edge(r, self.r):
            self.cv = 0
        elif _rising_edge(cu, self.cu) and self.cv < self._pv_max:
            self.cv += 1
        elif _rising_edge(ld, self.ld):
            self.cv = self.pv
        elif _rising_edge(cd, self.cd) and self.cv > self._pv_min:
            self.cv -= 1

        self.r = r
        self.pv = pv or self.pv
        self.cu = cu
        self.ld = ld
        self.cd = cd

        self.qu = self.cv >= self.pv
        self.qd = self.cv <= 0


class TP(FB):
    """Create an impulse."""

    def __init__(self, pt: float = 0.0):
        """
        pt: the impulse time
        """
        self.pt = pt
        self.start = False
        self.et = 0.0
        self.q = False
        self.start_time = None

    def __call__(self, start: bool = False, pt: float = 0.0):
        """Fire an impulse.

        start: start impulse (default False)
        pt: delay time in s (default 0.0)
        """
        if _rising_edge(start, self.start):
            # Take the time
            self.start_time = time.time()
            self.q = True
        elif self.start_time:
            # Timer is running
            now = time.time()
            diff = now - self.start_time
            self.et = diff
            if diff >= self.pt:
                # Timer has finished; reset variables
                self.start = False
                self.start_time = None
                self.et = 0.0
                self.q = False

        self.start = start
        self.pt = pt or self.pt


class TON(TP):
    """Create a delay in switching on."""

    def __init__(self, pt: float = 0.0):
        """
        pt: the delay time
        """
        return super().__init__(pt=pt)

    def __call__(self, start: bool = False, pt: float = 0.0):
        """Start the delay.

        start: start impulse (default False)
        pt: delay time in s (default 0.0)
        """
        if _rising_edge(start, self.start):
            # Take the time
            self.start_time = time.time()
        elif _falling_edge(start, self.start):
            # Impulse is low, reset timer
            self.start = False
            self.start_time = None
            self.et = 0.0
            self.q = False
        elif self.start_time:
            # Timer is running
            now = time.time()
            diff = now - self.start_time
            self.et = diff
            if diff >= self.pt:
                self.q = True

        self.start = start
        self.pt = pt or self.pt


class TOF(TP):
    """Create a delay in switching off."""

    def __init__(self, pt: float = 0.0):
        """
        pt: the delay time
        """
        super().__init__(pt=pt)
        self.q = True

    def __call__(self, start: bool = False, pt: float = 0.0):
        """Start the delay.

        start: start impulse (default False)
        pt: delay time in s (default 0.0)
        """
        if _rising_edge(start, self.start):
            # Take the time
            self.start_time = time.time()
        elif _falling_edge(start, self.start):
            # Impulse is low, reset timer
            self.start = False
            self.start_time = None
            self.et = 0.0
            self.q = True
        elif self.start_time:
            # Timer is running
            now = time.time()
            diff = now - self.start_time
            self.et = diff
            if diff >= self.pt:
                self.q = False

        self.start = start
        self.pt = pt or self.pt


class RS(FB):
    """A RS latch (reset dominance)."""

    def __init__(self):
        self.q = False
        self.r = False
        self.s = False

    def __call__(self, s: bool = False, r: bool = False) -> None:
        """Set or reset the latch.

        s: set signal (default False)
        r: reset signal (default False)
        """
        # Find out whether s or r are at a rising edge
        on = _rising_edge(s, self.s)
        off = _rising_edge(r, self.r)
        # Retain values
        self.s = s
        self.r = r
        self.q = (on or self.q) and not off


class SR(RS):
    """A SR latch (set dominance)."""

    def __init__(self):
        return super().__init__()

    def __call__(self, s: bool = False, r: bool = False) -> None:
        """Set or reset the latch.

        s: set signal (default False)
        r: reset signal (default False)
        """
        on = _rising_edge(s, self.s)
        off = _rising_edge(r, self.r)
        self.s = s
        self.r = r
        self.q = (self.q and not off) or on


class R_TRIG(FB):
    """Trigger on a rising flank."""

    def __init__(self):
        self.clk = False
        self.q = False

    def __call__(self, clk: bool):
        """Set the output q to True on a rising flank of the input signal.

        Reset q to False after one cycle.

        clk: the input signal
        """
        self.q = _rising_edge(clk, self.clk)
        self.clk = clk


class F_TRIG(R_TRIG):
    """Trigger on a falling flank."""

    def __init__(self):
        return super().__init__()

    def __call__(self, clk: bool):
        """Set the output q to True on a falling flank of the input signal.

        Reset q to False after one cycle.

        clk: the input signal
        """
        self.q = _falling_edge(clk, self.clk)
        self.clk = clk