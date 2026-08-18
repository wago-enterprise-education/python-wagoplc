---
layout: page
title: Python WAGO PLC Library - Development guide
lang: en
lang-ref: index
---

## Development guide

Welcome to the `python-wagoplc` development documentation! Here you'll find everything you need to know
about the library's internals.

### Development setup

This module uses [uv](https://docs.astral.sh/uv/) as the build system. First of all, [install uv](https://docs.astral.sh/uv/getting-started/installation/). To get the source code and set up a development environment, execute the following commands in your favourite terminal emulator:

```bash
git clone https://github.com/wago-enterprise-education/python-wagoplc
cd python-wagoplc
uv sync --group dev
source .venv/bin/activate
```

The last command activates the virtual environment created by `uv` and needs to be executed every time before you work on the project.

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

If you prefer to avoid shell activation, you can also use `uv run` for one-off commands such as `uv run python -m unittest discover -s tests`.

#### Library structure

Head over to [the internals documentation](internals.md) to become familiar with the inner workings
of this library.

### Tests

`python-wagoplc` uses `unittest` for testing purposes. To run all tests, in the project root folder execute the following command:

```bash
python -m unittest discover -s tests
```

You can also execute an individual test file directly using Python.

For a full overview of the available tests, coverage, prerequisites, and detailed test execution commands, see [Tests](tests.md).

#### Changelog

Every change made to the functionality of this library should have an entry in `CHANGELOG.md`.
Refer to this file for how to format your entry.

### Code linting

We use [`ruff`](https://docs.astral.sh/ruff/) for linting. Before you commit, run the checks with#:

```bash
ruff check --target-version py38
```

### Documentation with MkDocs

The documentation site, including the API reference, is built with [MkDocs](https://www.mkdocs.org/) and [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/). API pages are rendered directly from Python docstrings using [mkdocstrings](https://mkdocstrings.github.io/); there is no generated Markdown to commit.

To preview the documentation locally:

```bash
uv sync --group docs
uv run mkdocs serve
```

Documentation versions are managed with [mike](https://github.com/jimporter/mike) and published to the `gh-pages` branch.

#### Automated Workflow

- **Dev docs**: Deployed as the `dev` version on every push to `main` that touches `docs/`, `src/`, or `mkdocs.yml` (`docs-deploy-dev.yml`)
- **Release docs**: Deployed as a new version and updated as `latest` whenever a GitHub Release is created (`create-github-release.yml`)

---

Previous: [API Reference](api/api-reference.md)

Next: [Internals](internals.md)
