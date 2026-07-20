---
layout: page
title: Python WAGO PLC Library - Tests
lang: en
lang-ref: tests
---

## Tests

This document describes the current test suite of `python-wagoplc`:

The project tests are located in `tests/` and use Python's built-in `unittest` framework.
Some tests additionally use `pyfakefs` to simulate file system access without touching real PLC files.

Current test files:

- `tests/test_cc100.py`
- `tests/test_config.py`
- `tests/test_controller.py`
- `tests/test_tasks.py`

### `tests/test_cc100.py`

Focus: controller-level I/O behavior for CC100 variants.

Covered scenarios:

- Digital output writes (`digitalWrite`) including bitwise output state updates
- Digital input reads (`digitalRead`) with simulated process image changes
- Analog output writes (`analogWrite`) and analog input reads (`analogRead`)
- Validation for non-existing I/O addresses (warning behavior)
- Device-specific behavior for module `751-9403` (no analog inputs -> exception)

Notes:

- Uses `pyfakefs` to create fake file paths and calibration/process-image files.
- Prevents real hardware/file access in tests.

### `tests/test_config.py`

Focus: YAML configuration parsing and validation via `read_config`.

Covered scenarios:

- Missing configuration file
- Reading and instantiating variable mappings from YAML
- Resolving function blocks and handling unknown function block paths
- Task entry validation (missing callable, missing parameters)
- Required top-level configuration fields (for example `itemNumber`)
- Duplicate I/O mapping detection

Notes:

- Uses `unittest.mock.patch` for deterministic behavior.
- Creates temporary YAML/Python files during tests.

### `tests/test_controller.py`

Focus: `IOHandler` input/output image handling.

Covered scenarios:

- Rejecting input variables in output image processing
- Writing valid outputs via mocked controller write method
- Allowing and updating state variables

Notes:

- Uses a `DummyController` plus `Mock` objects.
- No real controller communication.

### `tests/test_tasks.py`

Focus: task registration and runtime behavior in `Tasks` and `Task`.

Covered scenarios:

- `@tasks.setup` contract validation (must return a dictionary)
- `@tasks.register` behavior and one-task-per-program rule
- Task initialization with callable entry functions
- Input/output variable inference for cycle functions
- Priority and sensitivity bounds validation
- Task cycle execution error behavior when no output is returned
- State variable update behavior over cycle execution

## Prerequisites

### Runtime requirements

- Python `>=3.8`

### Development/test dependencies

From `pyproject.toml`:

- `pyfakefs` (required by `tests/test_cc100.py`)
- Optional but recommended for development: `ruff`

### Recommended setup

Use `uv` (project default):

```bash
uv sync --group dev
source .venv/bin/activate
```

On Windows PowerShell, activate with:

```powershell
.venv\Scripts\Activate.ps1
```

## How to run tests manually

Run all tests from repository root:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

Run one test module:

```bash
python -m unittest tests.test_tasks -v
```

Run one test class:

```bash
python -m unittest tests.test_controller.TestIOHandler -v
```

Run one test method:

```bash
python -m unittest tests.test_config.Test_config.test_read_variables -v
```

## CI integration status

The repository now contains a dedicated workflow at `.github/workflows/run-tests.yml`.

The workflow runs automatically:

- on pushes to non-`main` branches when `src/**`, `tests/**`, `pyproject.toml`, or the workflow file itself changes
- on pull requests targeting `main` when the same relevant paths change
- manually via `workflow_dispatch`

CI execution details, including the current Python version matrix, are documented in [run-tests.md](../.github/workflows/run-tests.md).
The workflow uses `ubuntu-latest` as runner because parts of the current task handling code rely on Unix signals that are not available on Windows.
The results are stored in three places:

- console output in the workflow run
- a compact GitHub Actions job summary
- JUnit XML files uploaded as workflow artifacts
