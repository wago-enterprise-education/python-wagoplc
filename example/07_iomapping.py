# configure the io mapping and task from the config file
# yaml:
version: 0.2.0
connection: usb-c
ip: 192.168.42.42
port: 22
user: root
autoupdate: on
netmask: 255.255.255.0
gateway: undefined
io_mapping:
  pii:
    x12.di:
    x12.di1: endschalter
    x12.di2: di2
    x12.di3:
    x12.di4:
    x12.di5:
    x12.di6:
    x12.di7:
    x12.di8:
    x13.pt1: 
    x13.pt2: 
    x14.ai1: 
    x14.ai2: 
  piq:
    x5.do:
    x5.do1: motor
    x5.do2: do2
    x5.do3:
    x5.do4:
    x6.ao1: voltage
    x6.ao2:
tasks:
  - name: loop
    src: src
    entry: "main.loop"
    inputs: [endschalter, di2]
    outputs: [motor, do2, voltage]

# -----------------------------------------
# src/main.py

from wagoplc import WORD16

def loop(endschalter: bool, di2: bool) -> (bool, bool, WORD16):
    if endschalter:
        motor = False
        do2 = False
        voltage = 0
    else:
        motor = True
        do2 = True  
        voltage = 1000
    return motor, do2, voltage
