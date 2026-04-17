# Contributing guide

Thank you for considering a contribution to this project! Together we shall strive to make
`python-wagoplc` a stable, feature-rich and widely-used programming library.
Till then, it's still a long and rocky path, but rewarding! Check out [our roadmap](roadmap.md)
to find the next milestones.

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

## Documentation

The documentation is built using [Sphinx](https://www.sphinx-doc.org/). In order to build it locally, run the following command in the project root folder:

```bash
sphinx-build docs/ docs/_build docs/reference.rst
```

Automatic generation happens every time a commit is pushed to the `main` branch, using a GitHub Actions workflow.