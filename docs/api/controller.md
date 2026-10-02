<!-- markdownlint-disable -->

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/controller.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `controller`
Generic controller functionality. 

This module holds the controller factory and I/O wrapper classes for use by both the programmer and the library. 


- Controller: the controller base class from which every controller version inherits 
- IOHandler: handle the I/O wrapper classes and state variables for a task 
- IO: base class for an I/O interface, child classes: DI, DO, AI, AO, PT, NI, DIO, AIO 

**Global Variables**
---------------
- **LOG_FILE**


---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/controller.py#L29"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `IO`
Generic I/O superclass to store interface id. 

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/controller.py#L32"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(id: 'int', module: 'str' = '')
```

Save interface and module numbers. 

id: interface number module: module number 





---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/controller.py#L49"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `DI`




<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/controller.py#L32"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(id: 'int', module: 'str' = '')
```

Save interface and module numbers. 

id: interface number module: module number 





---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/controller.py#L51"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `DO`




<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/controller.py#L32"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(id: 'int', module: 'str' = '')
```

Save interface and module numbers. 

id: interface number module: module number 





---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/controller.py#L53"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `AI`




<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/controller.py#L32"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(id: 'int', module: 'str' = '')
```

Save interface and module numbers. 

id: interface number module: module number 





---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/controller.py#L55"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `AO`




<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/controller.py#L32"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(id: 'int', module: 'str' = '')
```

Save interface and module numbers. 

id: interface number module: module number 





---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/controller.py#L57"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `NI`




<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/controller.py#L32"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(id: 'int', module: 'str' = '')
```

Save interface and module numbers. 

id: interface number module: module number 





---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/controller.py#L59"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `PT`




<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/controller.py#L32"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(id: 'int', module: 'str' = '')
```

Save interface and module numbers. 

id: interface number module: module number 





---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/controller.py#L61"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `DIO`




<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/controller.py#L62"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(id: 'int', type: 'int', module: 'str' = '')
```









---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/controller.py#L65"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `AIO`




<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/controller.py#L62"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(id: 'int', type: 'int', module: 'str' = '')
```









---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/controller.py#L69"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Controller`
The controller interface and basic functionality. 

Needs to be implemented by every PLC added to the library. Each I/O function takes a module parameter referring to the controller module. It is forwarded to the controller specific _get_data and _set_data functions. 


- digitalWrite: write the digital outputs 
- analogWrite: write the analog outputs 
- digitalRead: read the digital inputs 
- analogRead: read the analog inputs 
- tempRead: read the temperature inputs 
- calibrateIn, calibrateOut, calibrateTemp: calibrate analog values 
- read_inputs: read and store controller inputs 
- write_outputs: write stored values to controller outputs 
- reset: reset all controller outputs 

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/controller.py#L88"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__()
```








---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/controller.py#L162"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `analogRead`

```python
analogRead(input: 'int', module: 'str') → int | bool
```

Read analog input and return calibrated value in mV. 

Return False if the analog input does not exist. 

input: Analog input to be read 

---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/controller.py#L119"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `analogWrite`

```python
analogWrite(output: 'int', voltage: 'int', module: 'str') → bool
```

Switch the output to the specified voltage. 

Return False if analog output does not exist, else return True. 

output: Analog output to be switched voltage: Voltage which the selected output should be set to 

---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/controller.py#L202"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `calibrateIn`

```python
calibrateIn()
```





---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/controller.py#L205"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `calibrateOut`

```python
calibrateOut()
```





---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/controller.py#L208"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `calibrateTemp`

```python
calibrateTemp()
```





---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/controller.py#L143"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `digitalRead`

```python
digitalRead(input: 'int', module: 'str') → int
```

Read the specified digital input and return the value as boolean. 

input: Digital input to be read 

---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/controller.py#L93"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `digitalWrite`

```python
digitalWrite(output: 'int', value: 'int', module: 'str') → bool
```

Switch the output to the specified value. 

output: Digital output to be switched value: Value which the selected output should be set to Return True if value is written, False if out does not exist. 

---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/controller.py#L211"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `read_inputs`

```python
read_inputs()
```

Fill the input image with actual data. 

---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/controller.py#L219"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `reset`

```python
reset()
```

Reset outputs and close any file descriptors. 

---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/controller.py#L174"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `tempRead`

```python
tempRead(input: 'int', module: 'str') → int
```

Read PT input and return calibrated value in °C. 

Return False if the PT input does not exist. 

input: PT input to be read 

---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/controller.py#L215"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `write_outputs`

```python
write_outputs()
```

Actually write the outputs from the output image. 


---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/controller.py#L224"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `IOHandler`
Handle the I/O wrapper classes. 


- get_input_image: get an input image (variables -> values) for a task cycle 
- process_output_image: process output variables of the cycle function and write outputs 
- update_timers: update state of running timers if the program was stopped for a while 
- read: read from a specific input interface 
- write: write to a specific output interface 

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/controller.py#L234"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(plc_object: 'Controller', var_mapping: 'dict[str, Any]')
```








---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/controller.py#L273"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_input_image`

```python
get_input_image(task: "'Task'") → dict[str, Any]
```





---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/controller.py#L281"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `process_output_image`

```python
process_output_image(task: "'Task'", output_image: 'dict[str, Any]') → None
```





---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/controller.py#L302"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `read`

```python
read(io: 'IO')
```





---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/controller.py#L244"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `set_task_vars`

```python
set_task_vars(task: "'Task'") → None
```

Set input variables and state variables for the given Task instance. 

Raise NotDefinedError if a parameter is not defined in the mapping. 

var_mapping: map of all user-defined variables  

---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/controller.py#L292"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `update_timers`

```python
update_timers(stop_duration: 'int')
```

Update start time of timer fbs, as program execution was paused. 

---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/controller.py#L310"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `write`

```python
write(io: 'IO', value: 'int | bool')
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
