# This example shows how to use a PLC program as a library.
from wagoplc import main

if __name__ == '__main__':
    main('plc_prg.py')

# ----------------

# The plc_prg.py file could look like this. Will be called by the main function above. (Arduino style)

from wagoplc import digitalread, digitalwrite

def setup():
    ...

def loop():

    di1 = digitalread(1)
    di2 = digitalread(2)
    do1 = digitalwrite(1, di1 and di2)
