<!-- markdownlint-disable -->

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/tasks.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `tasks`
Task management. 

This module holds the classes responsible for task management. 
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

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/tasks.py#L53"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    name: 'str',
    entry: 'Callable[, dict[str, str | int | bool]]',
    cycle_ms: 'int' = 100,
    priority: 'int' = 15,
    watchdog_ms: 'int' = 400000,
    sensitivity: 'int' = 0
)
```

Configure the task. 

Raise ValueError if priority or sensitivity are not within the allowed ranges. Raise NotDefinedError via _get_input_vars if there are undefined variables in the input parameters. 

name:        task name entry:       task function cycle_ms:    call cycle time in ms priority:    a priority from 1 (highest) to 15 watchdog_ms: maximum runtime in ms before watchdog interrupts sensitivity: sensitivity from 0 (highest) to 10 





---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/tasks.py#L109"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Scheduler`
A task scheduler. 


- run_tasks: run the collected tasks 

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/tasks.py#L115"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(
    tasks: 'list[Task]',
    iohandler: 'IOHandler',
    plc_obj: 'Controller'
) → None
```

Configure the scheduler. 

:param tasks: List of Task objects to run :param plc_obj: The controller object :param var_mapping: The complete variable mapping 




---

<a href="https://github.com/wago-enterprise-education/python-wagoplc/tree/main/src/wagoplc/tasks.py#L126"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run_tasks`

```python
run_tasks()
```

Scheduler to run all tasks in cycles. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
