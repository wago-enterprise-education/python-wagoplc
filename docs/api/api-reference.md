# API Overview

The API reference is rendered directly from the docstrings in `src/wagoplc`.

## Modules

- [`controller`](controller.md): Generic controller functionality.
- [`tasks`](tasks.md): Task management.
- [`fb`](fb.md): Standard function block library.
- [`constants`](constants.md): Top-level constants.
- [`exceptions`](exceptions.md): All library exceptions.
- [`read_config`](read_config.md): Configuration file loading.
- [`cc100`](cc100.md): Controller-specific functionality for the CC100.
- [`cc100.cc100_9301`](cc100.cc100_9301.md): The CC100 751-9301, the base version of the CC100 series.
- [`cc100.cc100_9401`](cc100.cc100_9401.md): The CC100 751-9401 with CAN support.
- [`cc100.cc100_9403`](cc100.cc100_9403.md): The CC100 751-9403 with DALI support, but without analog inputs.
- [`cc100.cc100_v1`](cc100.cc100_v1.md): Generic superclass for the older CC100 generation.
