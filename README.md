# Python WAGO PLC Library

[![Docs: Generate API Markdown with lazydocs](https://github.com/wago-enterprise-education/python-wagoplc/actions/workflows/generate-lazydocs.yml/badge.svg)](https://github.com/wago-enterprise-education/python-wagoplc/actions/workflows/generate-lazydocs.yml)
[![Build: Package with uv](https://github.com/wago-enterprise-education/python-wagoplc/actions/workflows/build-package.yml/badge.svg)](https://github.com/wago-enterprise-education/python-wagoplc/actions/workflows/build-package.yml)

[![Tests](https://img.shields.io/badge/tests-pytest-informational)](tests)

[![Python >=3.8](https://img.shields.io/badge/python-%3E%3D3.8-blue)](https://pypi.org/project/python-wagoplc/)
[![PyPI](https://img.shields.io/pypi/v/python-wagoplc)](https://pypi.org/project/python-wagoplc/)

Python WAGO PLC Library is a Python interface for interacting with WAGO PLCs (*Programmable Logic Controllers*). It lets you read and write controller data and build PLC applications in Python.

> [!CAUTION]
> **This repository is a development repository that was created as part of a student project and is not regularly maintained. It is neither a stable version nor an official repository of WAGO GmbH & Co. KG.**

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Function Blocks](#function-blocks)
- [Supported Controllers](#supported-controllers)
- [Usage Example](#usage-example)
  - [Configuration in the config file](#configuration-in-the-config-file)
  - [Configuration directly in the script](#configuration-directly-in-the-script)
- [Documentation](#documentation)
- [Development](#development)

## Features

- Fast cyclic execution with cycle times below 4 ms possible
- Easy configuration either in Python code or via `controller.yaml`
- Integration with the [VS Code Extension WAGO CC100](https://marketplace.visualstudio.com/items?itemName=WAGO-education.vscode-wago-cc100)
- IEC 61131-3 style standard function blocks for familiar PLC programming patterns
- Support for custom function blocks
- Multiple supported controller types

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

## Quick Start

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

Example application:

```python
# main.py
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

Run the application on the controller with:

```bash
python main.py
```

## Configuration

You can configure applications in two ways:

1. Script-first: define I/O, state variables, and task registration via `Tasks` decorators.
2. YAML-first: define I/O mapping, variables, and task metadata in `controller.yaml`.

When both are used, script-defined variables are merged with YAML-defined variables.

Example task configuration in YAML:

```yaml
tasks:
  - name: bottle buffer
    entry: main.bottle_buffer
    cycle_ms: 10
    priority: 15
    watchdog_ms: 400000
    sensitivity: 0
```

## Function Blocks

Included standard library blocks:

- Counters: CTU, CTD, CTUD
- Timers: TP, TON, TOF
- Latches and triggers: RS, SR, R_TRIG, F_TRIG

Custom function block classes can also be referenced from YAML using module-qualified names.

## Supported Controllers

> [!NOTE]
> Communication protocols such as RS485 serial interface, CANopen, and DALI are currently unsupported.

| Device | Firmware | Notes |
| :---- | :----: | :----: |
| 751-9301 | 30, 28 | |
| 751-9401 | 28 | |

## Usage Example

The library can model the same logic that is often written in a CODESYS program. A light barrier counts objects, and once a threshold is reached, the motor is stopped for a delay before it starts again.

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
    if process_delay.q:
        start_delay = False

    return dict(
        motor=motor,
        object_counter=object_counter,
        process_delay=process_delay,
        start_delay=start_delay,
    )

if __name__ == "__main__":
    main()
```

When configuration is done in configguration file, the individual I/O and variables are not defined in the script, but only referenced as function arguments. The `controller.yaml` file contains the actual variable definitions and I/O mapping:

```yaml
# controller.yaml 
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

@tasks.register(name="conveyor belt", cycle_ms=5)
def conveyor_belt(light_barrier, object_counter: CTU, process_delay: TON, start_delay):
    process_delay(start=start_delay)
    object_counter(cu=light_barrier, r=process_delay.q)

    motor = 5000
    if object_counter.q:
        motor = 0
        start_delay = True
    if process_delay.q:
        start_delay = False

    return dict(
        motor=motor,
        object_counter=object_counter,
        process_delay=process_delay,
        start_delay=start_delay,
    )

if __name__ == "__main__":
    main(tasks)
```

When configuration is done in the script, the only required entry in `controller.yaml` is the controller item number:

```yaml
# controller.yaml 
itemNumber: 751-9301
```

The WAGO CC100 VS Code extension can generate the controller config layout for supported devices.

## Documentation

- GitHub Pages: https://wago-enterprise-education.github.io/python-wagoplc/
- Documentation source: https://github.com/wago-enterprise-education/python-wagoplc/tree/main/docs

## Development

Local development uses `uv`:

```bash
uv sync
```

Useful follow-up commands:

```bash
pytest
uv run ruff check .
```

## License

See [LICENSE](LICENSE) for the license text.
