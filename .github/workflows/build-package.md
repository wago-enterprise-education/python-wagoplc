# Build Package Workflow

**File:** `build-package.yml`

## Overview

Builds Python distribution packages (wheel and source distribution) using [uv](https://docs.astral.sh/uv/) and automatically attaches them to GitHub releases. Supports both automated release builds and manual testing builds from any branch.

## Triggers

- **Release published** – Automatically when a GitHub release is created/published
- **Manual trigger** via `workflow_dispatch` (GitHub Actions UI) – For testing from any branch/tag

## What It Does

1. Checks out the repository
2. Installs `uv` build tool
3. Sets up Python 3.11
4. Builds distributions with `uv build`:
   - Wheel (`.whl`) – Binary distribution
   - Source distribution (`.tar.gz`) – Source package
5. Uploads distributions as workflow artifact `python-wagoplc-dist`
6. **On release:** Attaches distributions to the GitHub release

## Generated Artifacts

The build produces two package formats in `dist/`:

### Wheel (`.whl`)
```
dist/python_wagoplc-0.1.0-py3-none-any.whl
```
- Binary distribution – ready to install
- No compilation needed on user's machine
- Preferred format for pip installation

### Source Distribution (`.tar.gz`)
```
dist/python-wagoplc-0.1.0.tar.gz
```
- Original source code + metadata
- Allows custom builds or system integrations
- Required for PyPI and package managers

## Automatic Release Build

When you create a GitHub release:

1. Go to **Releases** → **Create a new release**
2. Set a tag and release name (e.g., `v0.2.0`)
3. Click **Publish release**
4. Workflow automatically:
   - Builds wheel and source distribution
   - Attaches both to the release
   - Makes them available for download

**Release download page will show:**
- `python_wagoplc-0.X.Y-py3-none-any.whl`
- `python-wagoplc-0.X.Y.tar.gz`

## Manual Build (Testing)

To build from any branch without releasing:

1. Go to **Actions** tab
2. Select **"Build: Package with uv"** workflow
3. Click **Run workflow**
4. Select branch/tag to build from
5. Download artifact `python-wagoplc-dist` after run completes

Manual builds **do not** attach to releases.

## Installation from Built Package

### From Released Wheel
```bash
pip install python_wagoplc-0.1.0-py3-none-any.whl
```

### From Released Source
```bash
pip install python-wagoplc-0.1.0.tar.gz
```

### From Local Build
```bash
uv build
pip install dist/python_wagoplc-*.whl
```

## Local Building

Build distributions locally without CI/CD:

```bash
# Install uv
pip install uv

# Or use the pre-installed uv from astral-sh/setup-uv action
uv build
```

Built packages appear in `dist/` directory.

## Build Configuration

Build settings are defined in `pyproject.toml`:

```toml
[build-system]
requires = ["uv_build>=0.8.19,<0.9.0"]
build-backend = "uv_build"

[project]
name = "wagoplc"
version = "0.1.0"
```

## Permissions

- **contents:** write – Create/modify release assets
- **id-token:** write – Authenticate with GitHub token

## PyPI Publishing (Future)

Once configured for PyPI, you can extend this workflow to automatically publish:

```yaml
# Example: Add after successful build
- name: Publish to PyPI
  uses: pypa/gh-action-pypi-publish@release/v1
  with:
    password: ${{ secrets.PYPI_API_TOKEN }}
```

## Troubleshooting

### Build fails with "module not found"
- Ensure `pyproject.toml` is valid
- Check that Python 3.11 is available
- Verify `src/wagoplc/` contains Python packages

### Wheel has wrong name
- Wheel name is generated from `pyproject.toml` metadata
- Update `name` and `version` fields if needed

### Release attachment failed
- Ensure release was created (not a draft)
- Check GitHub token permissions (contents: write needed)

## Related Files

- Build config: `pyproject.toml`
- Source code: `src/wagoplc/`
- Dependencies: `pyproject.toml` [project]
- Build system: `uv_build` backend
