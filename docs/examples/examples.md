---
layout: page
title: Python WAGO PLC Library - Examples
lang: en
lang-ref: index
---

This folder contains design and behavior examples for Python WAGO PLC programs.

## What you will find

- [arduino-style.py](arduino-style.py): Minimal Arduino-like API (`digitalRead` / `digitalWrite`) in one cyclic function.
- [variables.py](variables.py): Variable-based design with explicit setup mapping in Python.
- [variables_external.py](variables_external.py): Variable-based task where mapping is expected from external configuration.
- [cycle_time_example.py](cycle_time_example.py): Scheduler/watchdog behavior and timing model.
- [discussion.md](discussion.md): Pros/cons and the design rationale.

## Conceptual differences

### 1) Arduino-style approach

Reference: [arduino-style.py](arduino-style.py)

- Style: Imperative loop with direct I/O calls on an `io` object.
- Strengths: Very small and quick to read for users coming from Arduino.
- Trade-offs: Weak semantic naming for process signals, limited type hints/autocomplete, less PLC-like structure.

### 2) Variables in script

Reference: [variables.py](variables.py)

- Style: Define process variables in `setup()`, then use named parameters in cyclic tasks.
- Strengths: Clear mapping from hardware channels to descriptive process variables; better readability and maintainability.
- Trade-offs: More boilerplate and larger function signatures as projects grow.

### 3) Variables with external mapping

Reference: [variables_external.py](variables_external.py)

- Style: Keep Python logic lean; move I/O and variable mapping to a config file (for example `controller.yaml`).
- Strengths: Better for larger projects, easier generation/tooling support, portable configuration.
- Trade-offs: Adds indirection and a second source of truth to manage.

## Runtime behavior example

Reference: [cycle_time_example.py](cycle_time_example.py)

This example focuses on scheduler semantics:

- cycle time clamping and conversion from ms to seconds
- task priority ordering
- watchdog timeout checks
- sensitivity-based watchdog scaling

Use it to understand real-time constraints before tuning production task timings.

## Which example should I start with?

- New to PLC concepts and just want a minimal first run: start with [arduino-style.py](arduino-style.py).
- Building maintainable application logic in Python: use [variables.py](variables.py).
- Building larger or generated projects with stable deployment config: move toward [variables_external.py](variables_external.py).

## Recommendation

For this project, the preferred direction is variable-based design with script-first behavior and optional external configuration, as summarized in [discussion.md](discussion.md).
