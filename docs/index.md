# Python WAGO PLC Library

Python WAGO PLC Library is a Python interface for WAGO PLCs that lets you map controller I/O, read and write process values, and implement cyclic control logic in Python. It is designed for compact PLC applications, experiments with automation logic, and teaching environments that want to combine familiar PLC concepts with Python code.

> **Caution:** This repository is a development repository that was created as part of a student project and is not regularly maintained. It is neither a stable version nor an official repository of WAGO GmbH & Co. KG.

## Start here

Use the documentation in this order:

- [Getting Started](getting-started.md): Install the library, create a minimal project, write a first task, and run it on a supported controller.
- [User Guide](user-guide.md): Learn the configuration model, PLC concepts, and the typical ways to structure larger applications.
- [API Reference](api/api-reference.md): Look up modules, classes, functions, and controller abstractions.
- [Development Guide](development.md): Set up a local contributor environment, run checks, and work on the library itself.

## Typical use cases

- Build small PLC applications in Python around supported WAGO controllers.
- Map digital and analog I/O to named variables and cyclic task functions.
- Reuse IEC 61131-3 style function blocks such as counters, timers, and triggers.
- Prototype automation logic in code or split runtime configuration into `controller.yaml`.

## Documentation overview

### Getting Started

The getting-started guide focuses on the first successful run. It covers installation, the minimal project structure, the required `controller.yaml`, a first task script, and the two supported configuration styles.

[Go to Getting Started](getting-started.md)

### User Guide

The user guide explains the library's working model in more detail, including tasks, cycles, variable mapping, controller-specific usage, and practical application structure.

[Go to the User Guide](user-guide.md)

### API Reference

The API reference is the lookup section for modules such as `controller`, `tasks`, `fb`, and the controller-specific implementations.

[Go to the API Reference](api/api-reference.md)

### Development Guide

The development guide is intended for contributors. It covers local setup, tests, linting, and how the documentation and generated API pages are maintained.

[Go to the Development Guide](development.md)

## Additional resources

- [Examples](examples/examples.md): Small, focused examples for different application styles.
- [Internals](internals.md): Notes about the library's internal structure.
- [Tests](tests.md): Test overview and execution guidance.

---

Next: [Getting Started](getting-started.md)
