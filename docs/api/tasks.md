<!-- markdownlint-disable -->

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/tasks.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `tasks`
Task management. 

This module holds the classes responsible for task management. 
- Tasks: manage task and variable collection in an application script 
- Task: a single task 
- Scheduler: task scheduler 

**Global Variables**
---------------
- **LOG_FILE**
- **stop_time**
- **stop_duration**
- **task**

---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/tasks.py#L32"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `stop_handler`

```python
stop_handler(signum, frame)
```






---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/tasks.py#L39"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `cont_handler`

```python
cont_handler(signum, frame)
```






---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/tasks.py#L50"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Task`
Represent a PLC task. 


- cycle: one task cycle 

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/tasks.py#L56"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    plc_obj,
    var_mapping: dict[str, Any],
    name: str,
    entry: Callable[, dict[str, str | int | bool]],
    cycle_ms: int = 100,
    priority: int = 15,
    watchdog_ms: int = 400000,
    sensitivity: int = 0
)
```

Configure the task. 

Raise ValueError if priority or sensitivity are not within the allowed ranges. Raise NotDefinedError via _get_input_vars if there are undefined variables in the input parameters. 

name:        task name entry:       task function cycle_ms:    call cycle time in ms priority:    a priority from 1 (highest) to 15 watchdog_ms: maximum runtime in ms before watchdog interrupts sensitivity: sensitivity from 0 (highest) to 10 




---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/tasks.py#L133"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `cycle`

```python
cycle() → None
```

Run one task cycle. 


---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/tasks.py#L145"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Tasks`
Manage task registration per program. 

This class collects all variables, the task function and, if, given, its configuration. It can be instantiated in the main script. 

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/tasks.py#L153"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__()
```








---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/tasks.py#L171"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `register`

```python
register(
    _func: Callable[, dict[str, str | int | bool]] = None,
    name: str = '',
    cycle_ms: int = 100,
    watchdog_ms: int = 400000,
    priority: int = 15,
    sensitivity: int = 0
)
```

Register a task. Only one is currently allowed. 

name:        task name cycle_ms:    call cycle time in ms priority:    a priority from 1 (highest) to 15 entry:       task function watchdog_ms: maximum runtime in ms before watchdog interrupts sensitivity: sensitivity from 0 (highest) to 10 

---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/tasks.py#L158"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `setup`

```python
setup(func: Callable[[], dict[str, Any]]) → None
```

Retrieve variables from function in script. 

func: a function that returns all variables as a dict 


---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/tasks.py#L208"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Scheduler`
A task scheduler. 


- run_tasks: run the collected tasks 

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/tasks.py#L214"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(tasks: list[Task], plc_obj: Controller) → None
```

Configure the scheduler. 

tasks: list of task objects to run plc_obj: the controller object 




---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/tasks.py#L223"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run_tasks`

```python
run_tasks()
```

Scheduler to run all tasks in cycles. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
