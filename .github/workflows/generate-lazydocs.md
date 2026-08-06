# Generate API Docs Workflow

**File:** `generate-lazydocs.yml`

## Overview

Generates API reference Markdown from Python docstrings using `lazydocs` and updates `docs/api/` in the repository.

## Triggers

- Push to all branches (including `main`) when any of these paths change:
- `src/**`
- `pyproject.toml`
- `uv.lock`
- `.github/workflows/generate-lazydocs.yml`
- Manual trigger (`workflow_dispatch`)

## What It Does

1. Checks out repository history.
2. Sets up Python 3.11.
3. Forces `uv` to use Python 3.11 (`UV_PYTHON=3.11`) for compatibility with `lazydocs`.
4. Installs dependencies with `uv` using the `docs` dependency group from `pyproject.toml`.
5. Regenerates `docs/api/` with these options:

- `--output-path docs/api`
- `--overview-file api-reference.md`
- `--src-base-url https://github.com/wago-enterprise-education/python-wagoplc/tree/main`

1. Commits and pushes changes if generated files differ.
2. Uses `[skip ci]` in the bot commit message to avoid recursive workflow runs.
3. Uploads `docs/api` as artifact `api-docs-markdown`.

## Output

Generated files include:

- `docs/api/api-reference.md`
- Module pages under `docs/api/` (for example `controller.md`, `tasks.md`, `fb.md`)

## Required Permissions

- `contents: write` (commit and push generated docs)

## Local Run

```bash
uv sync --group docs
uv run --python 3.11 lazydocs \
  --output-path docs/api \
  --overview-file api-reference.md \
  --src-base-url "https://github.com/wago-enterprise-education/python-wagoplc/tree/main" \
  src/wagoplc
```

## Troubleshooting

### No commit created

- This is expected when generated output is unchanged.

### Workflow does not trigger on push

- Verify the push target branch is a branch ref (not only a tag push).
- Verify one of the configured paths changed.

### `AttributeError("'FileFinder' object has no attribute 'find_module'")`

- This typically means `lazydocs` ran on Python 3.12+.
- The workflow enforces Python 3.11 for `uv` to avoid this incompatibility.
