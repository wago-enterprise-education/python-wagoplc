# User guide

This guide provides you with general information and practical examples to work with the
`python-wagoplc` programming library.

## Integration with VS Code Extension WAGO CC100

The following examples show how to create PLC application scripts and configuration. In order to actually
run them, you'll need a CC100 of the first generation (before *751-9402*). In theory, transferring your project folder to the CC100 and running the following commands would be enough:

```bash
python -m pip install python-wagoplc
cd plc-application/
python main.py
```

Unfortunately, not all CC100 firmware versions have Python on board. Hence, a Docker image containing all
requirements and a [Python runtime](https://github.com/wago-enterprise-education/docker-engine-cc100) for WAGO PLCs has been created. It is highly recommended to make use of the [VS Code Extension WAGO CC100](https://marketplace.visualstudio.com/items?itemName=WAGO-education.vscode-wago-cc100), which installs that Docker image for you, transfers all files and manages the Docker container; you are then able to control your application by using the *operating-mode switch (OMS)* and watching the status lights, like with CoDeSys.

## The concept of PLC programming

PLC programming is standardised in IEC 61131-3. This library loosely adheres to that standard. Most importantly,
a PLC is a *multi-tasking system*: the kernel alternates between multiple *tasks*, which appears to the user as if they were concurrently executed. A task can also be triggered once by an event, or periodically (which is currently not supported). A single task execution is called a *cycle*. It has an input image (read from the controller inputs) and an internal state and produces an output image (written to the controller outputs).

Each task has a specific *cycle time* that defines the interval between executions as well as a priority.
Moreover, you can define a *watchdog*, which is the maximum time a task may take to execute before it is interrupted. A more advanced setting is the watchdog *sensitivity*. Each step adds a five percent tolerance to the watchdog time. See the docstring of the `Task` class for the allowed value ranges of these settings.

In this library, tasks are represented through Python functions: the function parameters are the input image,
the return value (a dictionary) the output image. To keep track of the internal state, variables need to be defined outside of the function, passed into it and also returned from it. Example:

```python
def task_function(di1, di2, state):
    # Do something with the variables
    state = 0
    do1 = True
    if di1:
        do1 = False
        state = 1

    # Return output and state variable
    # Key is variable name
    return dict(do1=do1, state=state)
```
For how to define the variables, see the examples below.

## One-script PLC application: bottle filling plant

At the bottle filling plant, the filled bottles are transferred to waiting crates using conveyor belts.
The full crates are afterwards loaded onto freight trains. To minimize the risk of delays or complications in this vital area, the plant contains a bottle buffer with a fixed capacity. Light barriers at the entrance and exit count the incoming and outgoing bottles. If the number of bottles exceeds the threshold, the motor is turned off.

The following steps show how to create the program for this plant using the WAGO PLC *751-9301*. You can find the whole source code [here](../plc-application/main.py).

### `main.py`

This script is the centerpiece of the PLC application, written by the programmer. It is directly invoked by the runtime. Thus, it must contain a call to the library's main function.
Initially, you'll want to define a few variables for later use. To access controller I/O, you can use wrapper classes. Example using an object of the `wagoplc.tasks.Tasks` class for collection of variables and tasks:

```python
from wagoplc import main, Tasks, DI, AO
from wagoplc.fb import CTUD

tasks = Tasks()

@tasks.setup
def setup():
    # Bind variable light_barrier_in to digital output 1
    light_barrier_in = DI(1)
    light_barrier_out = DI(2)
    motor = AO(1)
    # up-counter function block as per IEC 61131-3
    bottle_counter = CTUD(pv=150)

    return locals()
```
The `return locals()` statement creates a dictionary of variable names and values and returns it.
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
    # count up/down if a rising edge of the input variable is registered
    bottle_counter(cu=light_barrier_in, cd=light_barrier_out)
    # set to 5 V (5000 mV)
    motor = 5000
    # Counter has reached the threshold
    if bottle_counter.qu:
        # Turn motor off
        motor = 0

    # Return the output image
    return dict(motor=motor, bottle_counter=bottle_counter)
```
In the output iamge, the `motor` variable is mapped to an analog output and its value is written after every cycle, while the `bottle_counter` is considered a state variable. It is passed into the task function unchanged before the next cycle and therefore needs to be defined as a parameter.

### `controller.yaml`

This file holds the application's configuration. It is required to contain the `itemNumber` field with the controller's item number. Based on this information, the library selects the correct controller:

```yaml
itemNumber: 751-9301
```
With that, your application would be complete. But wait, there's more! You can also make use of the config file to define I/O mapping, state variables, and tasks, which keeps your `main.py` script slim:

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
    cycle_ms: 10
    priority:
    sensitivity:
    watchdog_ms:
```
Using this config, your `main.py` script would look like this:

```python
from wagoplc import main
from wagoplc.fb import CTUD

def bottle_buffer(light_barrier_in, light_barrier_out, bottle_counter: CTUD):
    bottle_counter(cu=light_barrier_in, cd=light_barrier_out, pv=150)
    motor = 5000
    if bottle_counter.qu:
        motor = 0

    return dict(motor=motor, bottle_counter=bottle_counter)

if __name__ == "__main__":
    main()
```

## Using own function blocks: factory gate control

A *function block (fb)* is a kind of module that takes a fixed set of input variables to determine a fixed set of
output variables. The programmer operates on instances of an fb in order to retain the internal state.
In the example above, you already used an up-counter function block from the standard library.
With `python-wagoplc`, you're also able to define your own function blocks for more complex setups.

Imagine having a large assembly hall with multiple entrance gates you need to control.
Each gate has an open and a close button as well as two limit switches.
Rather than duplicating the necessary code for each gate, you could employ a function block.

As always, your first step is to think about and define the variables and tasks you'll need, here in `controller.yaml`:

```yaml
itemNumber: 751-9301
  751-9301:
    pii:
      di1: open_btn
      di2: close_btn
      di3: limit_switch_left
      di4: limit_switch_right
    piq:
      do1: motor_open
      do2: motor_close
vars:
  - name: gate_control_fb
    # Retrieve class 'Gate_Control' from module 'gate_control.py'
    fb: gate_control.Gate_Control
tasks:
  - name: gate control
    entry: main.porta_westfalica
    cycle_ms: 20
    priority:
    sensitivity:
    watchdog_ms:
```
Next thing is to write `main.py`. In the following example, the input variables are collected and passed into a function block called `gate_control_fb`:

```python
from gate_control import Gate_Control

def porta_westfalica(
        gate_control_fb: Gate_Control, limit_switch_left,
        limit_switch_right, open_btn, close_btn):
    # Call to the function block
    gate_control_fb(open_btn, close_btn, limit_switch_left, limit_switch_right)
    print(gate_control_fb.open, gate_control_fb.closed)

    # Motors controlled through output variables
    return dict(gate_control_fb=gate_control_fb,
                motor_open=gate_control_fb.motor_open,
                motor_close=gate_control_fb.motor_close)
```

:::{note}
When you define your variables in the script, you can bind an instance of your fb to
the `gate_control_fb` variable directly (which is what the library does, internally).
:::

Now to the function block, which according to the above code is a class `Gate_Control` defined in a module
`gate_control.py` (in the same directory as `main.py` and `controller.yaml`). A function block in its current, simple form consists of a constructor setting any instance variables, and a `__call__()` method containing the actual functionality, which makes the instance callable:

```python
# Function block superclass
from wagoplc.fb import FB

class Gate_Control(FB):

    def __init__(self):
        self.open = False
        self.closed = True
        self.motor_open = False
        self.motor_close = False
        self.state = 0
    
    def __call__(self, open_btn: bool, close_btn: bool, 
        limit_switch_left: bool, limit_switch_right: bool):
        match self.state:
            case 0: # Gate closed
                if open_btn:
                    self.motor_open = True
                    self.closed = False
                    self.state = 1
            case 1: # Gate opens
                if not limit_switch_right:
                    self.motor_open = False
                    self.open = True
                    self.state = 2
            case 2: # Gate is open
                if close_btn:
                    self.motor_close = True
                    self.open = False
                    self.state = 3
            case 3: # Gate closes
                if not limit_switch_left:
                    self.motor_close = False
                    self.closed = True
                    self.state = 0
```



