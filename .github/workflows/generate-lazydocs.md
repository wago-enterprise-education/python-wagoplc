# Generate Lazydocs API Reference Workflow

**File:** `generate-lazydocs.yml`

## Overview

Automatically generates API reference documentation from Python source code using [lazydocs](https://github.com/ml-tooling/lazydocs). Generates Markdown files in `docs/api/` and provides them as workflow artifacts.

## Triggers

- **Push events** to any branch *except* `main` when:
  - Files in `src/**` are modified
  - `pyproject.toml` is modified
  - The workflow file itself changes
- **Manual trigger** via `workflow_dispatch` (GitHub Actions UI)

## What It Does

1. Checks out the repository
2. Sets up Python 3.11
3. Installs project dependencies and lazydocs
4. Runs lazydocs to generate API documentation:
   - Scans all modules in `src/wagoplc/`
   - Generates individual Markdown files for each module
   - Creates `README.md` overview file
   - Adds GitHub source code badges
5. Uploads generated files as workflow artifact `api-docs-markdown`

## Generated Output

Generated files are stored in `docs/api/`:

- `README.md` – API overview with links to all modules
- `*.md` – Individual module documentation:
  - `cc100.md` – CC100 controller implementations
  - `constants.md` – Module constants
  - `controller.md` – Controller base class and I/O interfaces
  - `exceptions.md` – Library exceptions
  - `fb.md` – Function blocks (CTU, CTUD, TON, etc.)
  - `read_config.md` – Configuration file parsing
  - `tasks.md` – Task scheduling and management

Each file includes:
- Module docstring and description
- Class and function definitions with signatures
- Parameter and return value documentation
- Links to source code on GitHub

## Local Generation

Generate API docs locally:

```bash
# Install lazydocs
pip install lazydocs

# Generate with overview and source links
lazydocs \
  --output-path docs/api \
  --overview-file README.md \
  --src-base-url "https://github.com/wago-enterprise-education/python-wagoplc/tree/main" \
  src/wagoplc
```

**Options used:**
- `--output-path docs/api` – Output directory
- `--overview-file README.md` – Generate overview file
- `--src-base-url` – Links source code badges to GitHub

## Accessing Artifacts

After the workflow runs:

1. Go to **Actions** tab on GitHub
2. Select **"Docs: Generate API Markdown (lazydocs)"** workflow
3. Click the latest run
4. Download the **`api-docs-markdown`** artifact
5. Extract and view `docs/api/README.md`

## Permissions

- **contents:** read – View repository contents

## Integration with Documentation

The generated API docs in `docs/api/` complement the Sphinx documentation:
- **Sphinx docs** (`sphinx.yml`): Conceptual guides and architecture
- **lazydocs** (`generate-lazydocs.yml`): Detailed API reference

For complete documentation, both need to be generated and deployed.

## Python Compatibility

- Generated for Python 3.8+ (compatible with project's minimum version)
- Runs on Python 3.11 in CI/CD

## Related Files

- Source code: `src/wagoplc/**/*.py`
- Configuration: `pyproject.toml`
- Python docstrings: Follow Google/NumPy style for best results
