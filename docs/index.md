---
layout: page
title: Python WAGO PLC Library
lang: en
lang-ref: index
---

This library provides a simple interface to interact with WAGO PLCs (-Programmable Logic Controllers*) using Python. It allows you to read and write data to the PLC, making it easier to integrate WAGO PLCs into your Python applications.

> **Caution:** This repository is a development repository that was created as part of a student project and is not regularly maintained. It is neither a stable version nor an official repository of WAGO GmbH & Co. KG.

## Content

- [Features](#features)
- [Quick start](#quick-start)
- [Configuration model](#configuration-model)
- [Function blocks](#function-blocks)
- [How it works](#how-it-works)
- [Documentation and examples](#documentation-and-examples)
- [Usage example](#usage-example)
  - [Configuration in the config file](#configuration-in-the-config-file)
  - [Configuration directly in the script](#configuration-directly-in-the-script)
- [Supported controllers](#supported-controllers)
- [Installation](#installation)

## Features

- blistering pace: cycle times of below 4ms possible
- easily configurable: directly in the script or via config file
- modern programming: seamless integration with the [VS Code Extension WAGO CC100](https://marketplace.visualstudio.com/items?itemName=WAGO-education.vscode-wago-cc100)
- familiar: CODESYS developers will feel at home in no time
- well-equipped: standard library of function blocks according to IEC 61131-3
- customizable: definition of own function blocks supported
- versatile: ever-growing list of supported controllers

## Quick start

Minimal project layout:

```text
plc-application/
  main.py
  controller.yaml
```

`controller.yaml` must at least define the controller item number:

```yaml
itemNumber: 751-9301
```

Basic task script:

```python
from wagoplc import main, Tasks, DI, AO
from wagoplc.fb import CTUD

tasks = Tasks()

@tasks.setup
def setup():
    light_barrier_in = DI(1)
    light_barrier_out = DI(2)
    motor = AO(1)
    bottle_counter = CTUD(pv=150)
    return locals()

@tasks.register(name="bottle buffer", cycle_ms=5)
def bottle_buffer(light_barrier_in, light_barrier_out, bottle_counter: CTUD):
    bottle_counter(cu=light_barrier_in, cd=light_barrier_out)
    motor = 0 if bottle_counter.qu else 5000
    return dict(motor=motor, bottle_counter=bottle_counter)

if __name__ == "__main__":
    main(tasks)
```

Run on target:

```bash
python main.py
```

## Configuration model

You can configure applications in two ways:

1. Script-first: define I/O, state variables, and task registration via `Tasks` decorators.
2. YAML-first: put I/O mapping, variables, and task metadata in `controller.yaml`.

When both are used, script-defined variables are merged with YAML-defined variables.

Example task section in YAML:

```yaml
tasks:
  - name: bottle buffer
    entry: main.bottle_buffer
    cycle_ms: 10
    priority: 15
    watchdog_ms: 400000
    sensitivity: 0
```

## Function blocks

Included standard library blocks:

- Counters: CTU, CTD, CTUD
- Timers: TP, TON, TOF
- Latches/triggers: RS, SR, R_TRIG, F_TRIG

You can also provide your own function block classes and reference them in YAML using module-qualified names.

## How it works

At runtime, the library:

1. Reads and validates the `controller.yaml`.
2. Loads variable mappings and tasks from YAML and/or script decorators.
3. Instantiates a controller implementation based on `itemNumber`.
4. Runs a scheduler that executes cyclic tasks, applies watchdog limits, and writes outputs.

## Documentation and examples

- [User guide](user-guide.md)
- [Internal architecture](internals.md)
- [Development setup and checks](development.md)
- [API Reference](api/api-reference.md)
- [Examples](examples/examples.md)

## Usage example

Consider the following CODESYS program, which operates a conveyor belt. A light barrier
registers every passing object and sends an impulse to the up-counter function block (CTU).
When the count value increases to 3, the motor is turned off for 4 seconds (processing time),
after which it is turned on again and the counter is reset.

```st
PROGRAM PLC_PRG
VAR
    xLightBarrier AT %IX0.0: BOOL;
    wMotor        AT %QW1  : INT; 
    oObject_counter_CTU: CTU;
    oDelay_TON: TON;
    start_delay: BOOL := False;
END_VAR

oDelay_TON(IN := start_delay, PT := 4, Q =>);
oObject_counter_CTU(CU := xLightBarrier, PV := 3, RESET:= oDelay_TON.Q, Q =>);

wMotor := 5000;
IF oObject_counter_CTU.Q THEN
   wMotor := 0
   start_delay := True;
END_IF
IF oDelay_TON.Q THEN
   start_delay := False;
END_IF
```

Of course, this snippet does not include the task configuration, which needs to be done
separately.

The following snippets show how the same could be programmed using this library.

### Configuration in the config file

```python
# main.py

from wagoplc import main
from wagoplc.fb import CTU, TON

def conveyor_belt(light_barrier, object_counter: CTU, process_delay: TON, start_delay):
    process_delay(start=start_delay, pt=4)
    object_counter(cu=light_barrier, r=process_delay.q, pv=3)

    motor = 5000
    if object_counter.q:
        motor = 0
        start_delay = True
        # Processing...
    if process_delay.q:
        # Resuming...
        start_delay = False

    return dict(motor=motor, object_counter=object_counter,
        process_delay=process_delay, start_delay=start_delay)

if __name__ == "__main__":
    main()
```

```yaml
# controller.yaml -- the bulk of this will be generated
...
# the controller item number
itemNumber: 751-9301
io_mapping:
  751-9301:
    pii:
      di1: light_barrier
      di2:
      di3:
      di4:
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
      do2:
      do3:
      do4:
      ao1: motor
      ao2:
vars:
  - name: object_counter
    fb: CTU
  - name: process_delay
    fb: TON
  - name: start_delay
    value: False
tasks:
  - name: Assembly line
    entry: main.conveyor_belt
    cycle_ms: 10
    priority:
    sensitivity:
    watchdog_ms:
```

### Configuration directly in the script

```python
# main.py

from wagoplc import main, Tasks, DI, AO
from wagoplc.fb import CTU, TON

tasks = Tasks()

@tasks.setup
def setup():
    light_barrier = DI(1)
    motor = AO(1)
    object_cnt = CTU(pv=2)
    process_delay = TON(pt=4)
    start_delay = False

    return locals()

@tasks.register(
        name = "conveyor belt",
        cycle_ms = 5
)
def conveyor_belt(light_barrier, object_counter: CTU, process_delay: TON, start_delay):
    process_delay(start=start_delay)
    object_counter(cu=light_barrier, r=process_delay.q)

    motor = 5000
    if object_counter.q:
        motor = 0
        start_delay = True
        # Processing...
    if process_delay.q:
        # Resuming...
        start_delay = False

    return dict(motor=motor, object_counter=object_counter,
        process_delay=process_delay, start_delay=start_delay)

if __name__ == "__main__":
    main(tasks)
```

```yaml
# controller.yaml -- needs to contain at least the controller item number
itemNumber: 751-9301
```

The WAGO CC100 VS Code extension will automatically generate the proper config-file layout for your
controller.

After transferring the script and configuration files, start your PLC application by simply running the following command on your controller:

```bash
python main.py
```

## Supported controllers

> **Note:** Communication protocols (RS485 serial interface, CANopen, DALI, ...) are currently unsupported.

|  Device  |  Firmware   |  Notes  |
|  :----   |  :----:     | :----:  |
| 751-9301 |  30,28      |         |
| 751-9401 |  28         |         |

## Installation

Python 3.8+ is required.

```bash
pip install python-wagoplc
```

For local development:

```bash
git clone https://github.com/wago-enterprise-education/python-wagoplc
cd python-wagoplc
uv sync
```

We recommend using it alongside the [VS Code Extension](https://marketplace.visualstudio.com/items?itemName=WAGO-education.vscode-wago-cc100), though, which provides an easy-to-use interface for communicating with the controller, as well as a runtime environment.
