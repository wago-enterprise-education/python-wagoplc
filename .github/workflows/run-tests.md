# Run Tests Workflow

This workflow automatically runs the project's unit tests for relevant code changes.

## Trigger

The workflow runs when one of the following events occurs:

- Push to any non-`main` branch if one of these paths changes:
  - `src/**`
  - `tests/**`
  - `pyproject.toml`
  - `.github/workflows/run-tests.yml`
- Pull request targeting `main` if one of these paths changes:
  - `src/**`
  - `tests/**`
  - `pyproject.toml`
  - `.github/workflows/run-tests.yml`
- Manual run via `workflow_dispatch`

## What it does

The workflow:

1. Checks out the repository.
2. Sets up Python 3.8, 3.9, 3.10, 3.11, 3.12, 3.13, and 3.14 via a matrix build.
3. Installs project and development dependencies using `uv sync --python ${{ matrix.python-version }} --frozen --group dev`.
4. Runs the `unittest` test suite from `tests/`.
5. Writes a short result summary to the GitHub Actions job summary.
6. Uploads the JUnit XML report as a workflow artifact.

The job runs on `ubuntu-latest` because parts of the current codebase use Unix signals such as `SIGUSR1`, which are not available on Windows.

## Test command

The suite is discovered from `tests/` using Python's built-in `unittest` loader.
JUnit XML output is generated with `unittest-xml-reporting`.

## Test result retention

- Console logs remain available in the workflow run.
- A concise summary is written directly to the run page.
- The XML report is uploaded as an artifact for 30 days.

This combination gives both fast human-readable feedback and a durable machine-readable test report.
