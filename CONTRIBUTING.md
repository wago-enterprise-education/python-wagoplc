# Contributing guide

Thank you for considering a contribution to this project! Together we shall strive to make
`python-wagoplc` a stable, feature-rich and widely-used programming library.
Till then, it's still a long and rocky path, but rewarding! Check out [our todo list](TODO.md)
to find the next milestones.

## Development setup

This module uses [uv](https://docs.astral.sh/uv/) as the build system. First of all, [install uv](https://docs.astral.sh/uv/getting-started/installation/). To get the source code and set up a development environment, execute the following commands in your favourite terminal emulator:

```bash
git clone https://github.com/wago-enterprise-education/python-wagoplc
cd python-wagoplc
uv sync
source .venv/bin/activate
```
The last command activates the virtual environment created by `uv` and needs to be executed every time before you work on the project.

## Tests

`python-wagoplc` uses `unittest` for testing purposes. To run all tests, in the project root folder execute the following command:

```bash
python -m unittest -s tests
```
You can also execute an individual test file directly using Python.

## Changelog

Every change made to the functionality of this library should have an entry in [`CHANGELOG.md`](CHANGELOG.md).
Refer to this file for how to format your entry.

## Library structure

Head over to [the development documentation](docs/development.md) to become familiar with the inner workings
of this library.