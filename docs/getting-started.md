# Getting Started

This guide walks through the shortest path from installation to a first running PLC application. It covers the minimum project structure, the required configuration file, a first cyclic task, and the two ways to configure an application.

## Before you begin

- Python 3.8 or newer is required.
- You need a supported WAGO controller such as the `751-9301` or `751-9401`.
- The [VS Code Extension WAGO CC100](https://marketplace.visualstudio.com/items?itemName=WAGO-education.vscode-wago-cc100) can help with deployment and configuration generation on supported devices.

> **Note:** Communication protocols such as RS485 serial interface, CANopen, and DALI are currently not supported.

## Installation

Install the package from PyPI:

```bash
pip install python-wagoplc
```

## Minimal project structure

Start with a small application folder:

```text
plc-application/
  main.py
  controller.yaml
```

The runtime script lives in `main.py`. The controller-specific configuration lives in `controller.yaml`.

## First configuration file

At minimum, `controller.yaml` must define the controller item number so the library can select the correct controller implementation:

```yaml
itemNumber: 751-9301
```

You can keep the rest of the application structure in Python first and add more YAML configuration later.

## First application

The following example creates a small cyclic task that reads two digital inputs, updates a counter function block, and writes an analog output:

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

Save this as `main.py` in your project folder.

## Run the script

Run the application from the directory that contains `controller.yaml` with:

```bash
python main.py
```

The library reads `controller.yaml` from the current working directory, selects the controller implementation from `itemNumber`, and starts the registered cyclic tasks.

## Two configuration approaches

You can structure applications in two different ways.

### Script-first

Define I/O, state variables, and task registration directly in Python by using `Tasks`, `setup()`, and `@tasks.register(...)`.

Use this style when you want:

- the full application structure close to the Python code
- quick experiments and prototypes
- minimal YAML beyond the controller item number

### YAML-first

Move I/O mapping, variables, and task metadata into `controller.yaml`, while the Python script contains the task logic.

Example task definition in YAML:

```yaml
tasks:
  - name: bottle buffer
    entry: main.bottle_buffer
    cycle_ms: 10
    priority: 15
    watchdog_ms: 400000
    sensitivity: 0
```

Use this style when you want:

- clearer separation between runtime logic and deployment configuration
- generated or centrally maintained configuration files
- a slimmer task script

When both styles are used together, script-defined variables are merged with YAML-defined variables.

## Core concepts

### Tasks

A PLC application is executed as one or more cyclic tasks. In this library, a task is a Python function that reads input values and returns the output and state values for the next cycle.

### I/O mapping

I/O mapping connects physical controller channels such as `DI(1)` or `AO(1)` to descriptive variables used in your task logic. This mapping can live directly in Python or in `controller.yaml`.

### Function blocks

The `wagoplc.fb` module provides IEC 61131-3 style function blocks such as counters, timers, latches, and triggers. They let you implement common PLC control patterns without building every state machine from scratch.

## Where to go next

- Read the [User Guide](user-guide.md) for the full PLC programming model and more extensive examples.
- Browse the [Examples](examples/examples.md) for different application styles.
- Use the [API Reference](api/api-reference.md) when you need details about specific classes and functions.

---

Previous: [Documentation Home](index.md)

Next: [User Guide](user-guide.md)
