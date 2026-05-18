# Build Package Workflow

**File:** `build-package.yml`

## Overview

Builds Python distribution packages (wheel and source distribution) with [uv](https://docs.astral.sh/uv/).

The workflow supports two modes:

1. Automatic build when a release is created.
2. Manual build with an optional commit SHA.

On release builds, generated files are uploaded to the GitHub release.
On manual builds, generated files are uploaded as workflow artifacts.

## Triggers

- Release created (`release.types: [created]`)
- Manual trigger (`workflow_dispatch`)

Manual trigger input:

- `commit_sha` (optional): specific commit to build

If `commit_sha` is empty, the workflow builds the selected branch/tag HEAD.

## Workflow Name

The workflow appears in GitHub Actions as:

- `Build Python Package`

## What It Does

1. Checks out the repository at `inputs.commit_sha` or `github.sha`.
2. On manual runs, extracts version from `pyproject.toml` and computes short commit hash.
3. Creates manual artifact name format: `python-wagoplc-dist-v<version>-<short-hash>`.
4. Sets up Python 3.11.
5. Installs `uv`.
6. Cleans old build outputs (`dist`, `build`, `*.egg-info`).
7. Verifies uv cache availability.
8. Installs dependencies with `uv sync --frozen`.
9. Builds package files with `uv build`.
10. Validates that both `.whl` and `.tar.gz` exist in `dist/`.
11. Uploads output:

- Release run: uploads `dist/*` to the release assets.
- Manual run: uploads `dist/*` as workflow artifact (retention 30 days).

## Generated Files

Expected build outputs in `dist/`:

```text
dist/python_wagoplc-<version>-py3-none-any.whl
dist/python-wagoplc-<version>.tar.gz
```

## Automatic Release Build

When creating a GitHub release:

1. Go to Releases and create a new release.
2. Set tag and release title.
3. Publish the release.
4. Workflow builds package files and uploads them as release assets.

## Manual Build

To build without creating a release:

1. Open Actions.
2. Select `Build Python Package`.
3. Click Run workflow.
4. Optionally provide `commit_sha`.
5. Download artifact after completion.

Manual artifact naming:

```text
python-wagoplc-dist-v<version>-<short-commit-hash>
```

## Local Build

```bash
uv build
```

Output files are placed in `dist/`.

## Build Configuration

Build metadata comes from `pyproject.toml`.

```toml
[build-system]
requires = ["uv_build>=0.8.19,<0.9.0"]
build-backend = "uv_build"

[project]
name = "wagoplc"
version = "0.1.0"
```

## Permissions

Required workflow permissions:

- `contents: write`

## Troubleshooting

### Missing build files in `dist/`

- Confirm `uv build` succeeds locally.
- Confirm `pyproject.toml` is valid.

### Release asset upload failed

- Ensure the release event is `created`.
- Ensure workflow has `contents: write` permission.

### Manual build used wrong revision

- Verify `commit_sha` exists in the repository.
- If `commit_sha` is empty, verify selected branch/tag before running.

## Related Files

- `pyproject.toml`
- `src/wagoplc/`
- `.github/workflows/build-package.yml`
