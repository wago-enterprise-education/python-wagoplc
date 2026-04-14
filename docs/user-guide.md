# User guide

This guide provides you with general information and practical examples to work with the
`python-wagoplc` programming library.

## One-script PLC application: bottle filling plant

At the bottle filling plant, the filled bottles are transferred to waiting crates using conveyor belts.
The full crates are afterwards loaded onto freight trains. To minimize the risk of delays or complications in this vital area, the plant contains a bottle buffer with a fixed capacity. Light barriers at the entrance and exit count the incoming and outgoing bottles. If the number of bottles exceeds the threshold, the motor is turned off.

The following steps show how to create the program for this plant using the WAGO PLC *751-9301*. You can find the whole source code [here](../plc-application/main.py).

### `main.py`

This script is the centerpiece of the PLC application, written by the programmer. It is directly invoked by the runtime. Thus, it must contain a call to the library's main function.
Initially, you'll want to define a few variables for later use. You can do this using a function and an object of the `wagoplc.tasks.Tasks` class:

```python
from wagoplc import main, Tasks, DI, AO
from wagoplc.fb import CTUD

tasks = Tasks()

@tasks.setup
def setup():
    light_barrier_in = DI(1)
    light_barrier_out = DI(2)
    motor = AO(1)
    # up-counter function block as per IEC 61131-3
    bottle_counter = CTUD(pv=150)

    return locals()
```
The light barriers and the motor are mapped to I/O using wrapper classes.
The `return locals()` statement creates a dictionary of variable names and value and returns it.
It is collected by the setup decorator and saved in the `Tasks` object.

Now, you write the actual program as a Python function, which represents a PLC task.
Task-related settings like the name and cycle time can be defined via another decorator:

```python
@tasks.register(
        name = "bottle buffer",
        # Cycle time of 5ms
        cycle_ms = 5
)
def bottle_buffer(light_barrier_in, light_barrier_out, bottle_counter: CTUD):
    bottle_counter(cu=light_barrier_in, cd=light_barrier_out)
    # set to 5 V (5000 mV)
    motor = 5000
    if bottle_counter.qu:
        # Turn motor off
        motor = 0

    # Return the output image
    return dict(motor=motor, bottle_counter=bottle_counter)
```
In the output iamge, the `motor` variable is mapped to an analog output and its value is written after every cycle, while the `bottle_counter` is considered a state variable. It is passed into the task function unchanged in the next cycle and therefore needs to be defined as a parameter.

Last, but not least, your script needs to contain a call to the `main` function provided by the `python-wagoplc`
library, since it is directly invoked by the runtime:

```python
# Only run this if the script is directly executed
if __name__ == "__main__":
    main(tasks)
```
Here, the tasks object is passed to the function. At this point, it holds both the variables and the task definition.

### `controller.yaml`

This file holds the application's configuration. It is required to contain the `itemNumber` field with the controller's item number. Based on this information, the library selects the correct controller:

```yaml
itemNumber: 751-9301
```
With that, your application would be complete. But wait, that's not all! You can also make use of the config file to define I/O mapping, state variables, and tasks, which keeps your `main.py` script slim:

```yaml
io_mapping:
  # Module name; for the CC100 controllers, the item number
  751-9301:
    # input image
    pii:
      di1: light_barrier_in
      di2: light_barrier_out
    # output image
    piq:
      ao1: motor
# state variables
vars:
  - name: bottle_counter
    fb: CTUD
tasks:
  - name: bottle buffer
    # Script entry point
    entry: main.bottle_buffer
    # Cycle time
    cycle_ms: 50
    priority:
    sensitivity:
    watchdog_ms:
```
Using this config, your `main.py` script would look like this:

```python
from wagoplc import main
from wagoplc.fb import CTUD

def bottle_buffer(light_barrier_in, light_barrier_out, bottle_counter: CTUD):
    bottle_counter(cu=light_barrier_in, cd=light_barrier_out)
    motor = 5000
    if bottle_counter.qu:
        motor = 0

    return dict(motor=motor, bottle_counter=bottle_counter)

if __name__ == "__main__":
    main()
```

