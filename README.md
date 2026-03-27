# Python WAGO PLC Library

This library provides a simple interface to interact with WAGO PLCs (*Programmable Logic Controllers*) using Python. It allows you to read and write data to the PLC, making it easier to integrate WAGO PLCs into your Python applications.

> [!CAUTION]
> **This repository is a development repository that was created as part of a student project and is not regularly maintained. It is neither a stable version nor an official repository of WAGO GmbH & Co. KG.**

## Features

* blistering pace: cycle times of below 4ms possible
* easily configurable: directly in the script or via config file
* modern porgramming: seamless integration with the [VS Code Extension WAGO CC100](https://marketplace.visualstudio.com/items?itemName=WAGO-education.vscode-wago-cc100)
* familiar: CoDeSys developers will feel at home in no time
* well-equipped: standard library of function blocks according to IEC 61131-3
* customizable: definition of own function blocks
* versatile: ever-growing list of supported controllers

## Usage example

Consider the following CoDeSys program, which controls a light using an on and an off switch:

```
PROGRAM light_control
VAR
    oLight_On_RS: RS;
    iStatus: INT;
END_VAR

oLight_On_RS(R := xSwitch, S := xSwitch_off, Q =>);
CASE iStatus OF
    0:      IF oLight_On_RS.Q THEN
                xLight := True;
                iStatus := 1;
            END_IF
    1:      IF NOT oLight_On_RS.Q THEN
                xLight := False;
                iStatus := 0;
            END_IF
END_CASE
```
Of course, this snippet does not include the I/O mapping and task configuration, which need to be done
in separate areas of the CoDeSys development system.

The following snippets show how the same could be programmed using this library.

### Configuration in the config file

```python
# main.py

from wagoplc.fb import RS

def light_ctrl(oLight_On_RS: RS, xSwitch: bool, xSwitch_off: bool, iStatus: int):
    oLight_On_RS(s=xTSwitch, r=xSwitch_off)
    match iStatus:
        case 0:
            if oLight_On_RS.q:
                xLight = True
                iStatus = 1
        case 1:
            if not oLight_On_RS.q:
                xLight = False
                iStatus = 0

    return dict(oLight_On_RS=oLight_On_RS, xLight=xLight, iStatus=iStatus)
```

```yaml
# controller.yaml -- the bulk of this will be generated
...
# the controller item number
itemNumber: 751-9301
io_mapping:
  751-9301:
    pii:
      di1:
      di2:
      di3: xTaster
      di4: xTaster_Aus
      di5:
      di6:
      di7:
      di8:
      pt1: 
      pt2: 
      ai1: 
      ai2: 
    piq:
      do1:
      do2: xLuefter
      do3:
      do4:
      ao1:
      ao2:
vars:
  - name: oLight_On_RS
    fb: RS
  - name: iStatus
    value: 0
tasks:
  - name: Control the light
    entry: main.light_ctrl
    cycle_ms: 10
    priority:
    sensitivity:
    watchdog_ms:
```

### Configuration directly in the script

```python
# main.py

from wagoplc import DI, main, Tasks
from wagoplc.fb import RS

tasks = Tasks()

# Define the task variables
@tasks.setup
def setup():
    oLight_On_RS = RS()
    xSwitch = DI(1)
    xSwitch_off = DI(2)
    xLight = DO(1)

    return locals()

# Register the task
@tasks.register(
    name="Control the light",
    cycle_ms="10"
)
def light_ctrl(oLight_On_RS: RS, xSwitch: bool, xSwitch_off: bool, iStatus: int):
    oLight_On_RS(s=xTSwitch, r=xSwitch_off)
    match iStatus:
        case 0:
            if oLight_On_RS.q:
                xLight = True
                iStatus = 1
        case 1:
            if not oLight_On_RS.q:
                xLight = False
                iStatus = 0

    # Return the variables for processing
    return dict(oLight_On_RS=oLight_On_RS, xLight=xLight, iStatus=iStatus)

# Let the library take over
if __name__ == "__main__":
    main(tasks)
```

```yaml
# controller.yaml -- needs to contain at least the controller item number
itemNumber: 751-9301
```

The WAGO CC100 VS Code extension will automatically generate the proper config-file layout for your
controller.

After transferring the necessary files, start your PLC script by simply running the following command on your controller:

```
python main.py
```

## Supported controllers

> [!NOTE]
> Communication protocols (RS485 serial interface, CANopen, DALI, ...) are at the time unsupported.

|  Device  |  Notes   |
|  :----   |  :----:  |
| 751-9301 |          |

## Installation

You can (hopefully soon) install this library from the Python package index:

```
pip install python-wagoplc
```

We recommend using it alongside the [VS Code Extension](https://marketplace.visualstudio.com/items?itemName=WAGO-education.vscode-wago-cc100), though, which provides an easy-to-use interface for communicating with
the controller, as well as a runtime environment.

## Contributing

Contributions of all kind are very welcome! To get you started, head over to our [contributing instructions](CONTRIBUTING.md).