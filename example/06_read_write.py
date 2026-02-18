# This example shows how to use a PLC program as a library.
from wagoplc import main

if __name__ == '__main__':
    main('plc_prg.py')

# ----------------

# The plc_prg.py file could look like this. Will be called by the main function above. (Arduino style)

from wagoplc import read, write

def setup():
    ...

def loop():
    pii = read('di1', 'di2')

    di1 = pii['di1']
    di2 = pii['di2']

    do1 = write(dict(
        do1 = di1 and di2
    ))
