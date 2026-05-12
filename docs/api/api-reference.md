<!-- markdownlint-disable -->

# API Overview

## Modules

- [`cc100`](./cc100.md#module-cc100): Controller-specific functionality for the CC100.
- [`cc100.cc100_9301`](./cc100.cc100_9301.md#module-cc100cc100_9301): The CC100 751-9301 is the base version of the CC100 series. 
- [`cc100.cc100_9401`](./cc100.cc100_9401.md#module-cc100cc100_9401): The CC100 751-9401 with CAN support.
- [`cc100.cc100_9403`](./cc100.cc100_9403.md#module-cc100cc100_9403): The CC100 751-9403 with DALI support, but without analog inputs.
- [`cc100.cc100_v1`](./cc100.cc100_v1.md#module-cc100cc100_v1): Generic superclass for the older CC100 generation.
- [`constants`](./constants.md#module-constants): Top-level constants.
- [`controller`](./controller.md#module-controller): Generic controller functionality.
- [`exceptions`](./exceptions.md#module-exceptions): All library exceptions.
- [`fb`](./fb.md#module-fb): Standard library.
- [`read_config`](./read_config.md#module-read_config): wagoplc.read_config
- [`tasks`](./tasks.md#module-tasks): Task management.

## Classes

- [`cc100_9301.CC100_9301`](./cc100.cc100_9301.md#class-cc100_9301)
- [`cc100_9401.CC100_9401`](./cc100.cc100_9401.md#class-cc100_9401)
- [`cc100_9403.CC100_9403`](./cc100.cc100_9403.md#class-cc100_9403)
- [`cc100_v1.CC100_v1`](./cc100.cc100_v1.md#class-cc100_v1)
- [`controller.AI`](./controller.md#class-ai)
- [`controller.AIO`](./controller.md#class-aio)
- [`controller.AO`](./controller.md#class-ao)
- [`controller.Controller`](./controller.md#class-controller): The controller interface and basic functionality.
- [`controller.DI`](./controller.md#class-di)
- [`controller.DIO`](./controller.md#class-dio)
- [`controller.DO`](./controller.md#class-do)
- [`controller.IO`](./controller.md#class-io): Generic I/O superclass to store interface id.
- [`controller.IOHandler`](./controller.md#class-iohandler): Handle the I/O wrapper classes.
- [`controller.NI`](./controller.md#class-ni)
- [`controller.PT`](./controller.md#class-pt)
- [`exceptions.InvalidConfigError`](./exceptions.md#class-invalidconfigerror): Throw when an invalid configuration was given.
- [`exceptions.NonExistingIOError`](./exceptions.md#class-nonexistingioerror): Throw when a not existing IO is trying to be reached.
- [`exceptions.NotDefinedError`](./exceptions.md#class-notdefinederror): Raised when a variable in a task function is not defined in IO mapping.
- [`exceptions.WAGOPlcError`](./exceptions.md#class-wagoplcerror): Base class for WAGO PLC related errors.
- [`exceptions.WatchdogTimeoutError`](./exceptions.md#class-watchdogtimeouterror): Throw when task cycle exceeds maximum allowed time.
- [`fb.CTD`](./fb.md#class-ctd): A down-counter function block.
- [`fb.CTU`](./fb.md#class-ctu): An up-counter function block.
- [`fb.CTUD`](./fb.md#class-ctud): An up- and down-counter function block.
- [`fb.FB`](./fb.md#class-fb): Generic superclass for a function block.
- [`fb.F_TRIG`](./fb.md#class-f_trig): Trigger on a falling flank.
- [`fb.RS`](./fb.md#class-rs): A RS latch (reset dominance).
- [`fb.R_TRIG`](./fb.md#class-r_trig): Trigger on a rising flank.
- [`fb.SR`](./fb.md#class-sr): A SR latch (set dominance).
- [`fb.TOF`](./fb.md#class-tof): Create a delay in switching off.
- [`fb.TON`](./fb.md#class-ton): Create a delay in switching on.
- [`fb.TP`](./fb.md#class-tp): Create an impulse.
- [`tasks.Scheduler`](./tasks.md#class-scheduler): A task scheduler.
- [`tasks.Task`](./tasks.md#class-task): Represent a PLC task.
- [`tasks.Tasks`](./tasks.md#class-tasks): Manage task registration per program.

## Functions

- [`read_config.get_controller`](./read_config.md#function-get_controller): Get controller object by item number.
- [`read_config.read_config`](./read_config.md#function-read_config): Read the configuration file.
- [`read_config.validate_task`](./read_config.md#function-validate_task): Validate task schema.
- [`tasks.cont_handler`](./tasks.md#function-cont_handler)
- [`tasks.stop_handler`](./tasks.md#function-stop_handler)


---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
