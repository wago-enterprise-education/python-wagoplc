---
layout: page
title: Python WAGO PLC Library - internals
lang: en
lang-ref: index
---

This page describes the internal structure of the `python-wagoplc` library. 

## Mode of operation

What happens if you run `python main.py` at the command line? The following graphic illustrates the internal workflow.

![python-wagoplc internal workflow](work_schedule.svg)

The top-level `__init__.py` file contains the `main()` function, which is called when the application script executes. It is responsible for reading the configuration, creating a `Scheduler` instance and starting the task execution cycle.

### Configuration handling

The `read_config` module contains a function of the same name, which is called by the `main()` function.
It reads the configuration file `controller.yaml` and interprets an optional `Tasks` instance given from the script.
With this in mind, it creates a unified variable mapping, a `Controller` object and a list of `Task` objects.
In the process, any invalid configuration is identified and results in an exception. This involves validating the schema of the `tasks` section using the [`schema` library](https://pypi.org/project/schema/).

### Task management

Task management happens inside the `tasks` module, which contains the `Tasks`, `Task` and `Scheduler` classes.
At the moment, the scheduler supports running cyclic tasks, with support for event-based and periodic tasks planned.
It runs until an external interrupt occurs, after which the PLC outputs are reset and any open file descriptors closed.

### Standard library

`python-wagoplc` also contains a standard library of function blocks as defined by IEC 61131-3, which can be imported
from the `fb` module. The function block object is created behind the scenes in `read_config`, which imports the corresponding class either from the standard library or a user-defined module.

### Controller-specific functionality

At the heart of the `python-wagoplc` are the packages that define controller-specific functionality. Each controller series must have its own package, each controller must have its own module and class. The first and base controller of a series must both define the `Controller` interface and be a superclass for each following version, if applicable. Inside a controller package, controllers may also be grouped into generations. See the `CC100_v1` class and its subclasses as an example.
