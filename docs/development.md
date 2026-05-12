---
layout: page
title: Python WAGO PLC Library - Development guide
lang: en
lang-ref: index
---

Welcome to the `python-wagoplc` development documentation! Here you'll find everything you need to know
about the library's internals.

## Development setup

This module uses [uv](https://docs.astral.sh/uv/) as the build system. First of all, [install uv](https://docs.astral.sh/uv/getting-started/installation/). To get the source code and set up a development environment, execute the following commands in your favourite terminal emulator:

```bash
git clone https://github.com/wago-enterprise-education/python-wagoplc
cd python-wagoplc
uv sync --group docs
source .venv/bin/activate
```

The last command activates the virtual environment created by `uv` and needs to be executed every time before you work on the project.

## Library structure

Head over to [the internals documentation](internals.md) to become familiar with the inner workings
of this library.

## Tests

`python-wagoplc` uses `unittest` for testing purposes. To run all tests, in the project root folder execute the following command:

```bash
python -m unittest discover -s tests
```

You can also execute an individual test file directly using Python.

## Changelog

Every change made to the functionality of this library should have an entry in `CHANGELOG.md`.
Refer to this file for how to format your entry.

## Code linting

We use [`ruff`](https://docs.astral.sh/ruff/) for linting. Before you commit, run the checks with:

```bash
ruff check --target-version py38
```

## API Reference with lazydocs

The API reference is generated from Python docstrings using [lazydocs](https://github.com/ml-tooling/lazydocs). See the [API reference](api/api-reference.md) for the generated docs.

To generate locally:

```bash
lazydocs \
  --output-path docs/api \
  --overview-file api-reference.md \
  --src-base-url "https://github.com/wago-enterprise-education/python-wagoplc/tree/main" \
  src/wagoplc
```

### Automated Workflow

- **lazydocs generation**: Triggered on push to all branches except `main` when `src/` or `pyproject.toml` changes; artifacts available in workflow runs via `generate-lazydocs.yml`
