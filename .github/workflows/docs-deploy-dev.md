# Deploy Dev Docs Workflow

**File:** `docs-deploy-dev.yml`

## Overview

Builds the MkDocs documentation site and deploys it as the `dev` version to the `gh-pages` branch using [mike](https://github.com/jimporter/mike).

## Triggers

- Push to `main` when any of these paths change:
  - `docs/**`
  - `src/**`
  - `mkdocs.yml`
  - `pyproject.toml`
  - `.github/workflows/docs-deploy-dev.yml`
- Manual trigger (`workflow_dispatch`)

## What It Does

1. Checks out repository history (`fetch-depth: 0`, required for the `gh-pages` branch history used by `mike`).
2. Installs dependencies with `uv` using the `docs` dependency group from `pyproject.toml`.
3. Runs `mike deploy --push dev`, which builds the site with MkDocs and commits it to `gh-pages` under the `dev` version, without touching the `latest` alias used by releases.

## Required Permissions

- `contents: write` (push to `gh-pages`)

## Local Run

```bash
uv sync --group docs
uv run mkdocs serve
```

## Related Workflows

- Complements: [create-github-release.md](create-github-release.md) (deploys versioned release docs and updates `latest`)
