# GitHub Actions Workflows

This directory contains the CI/CD workflows used by `python-wagoplc`.

## Release Flow

The release automation is organized as follows:

```text
1. Start Release Branch (Manual) 
   ↓
2. Development & Testing on release/v* branch
   ↓
3. Generate API Markdown with lazydocs (Automatic - triggered by push to release/v* when src/ changes)
   ↓  
4. Create Pull Request (release/v* → main)
   ↓
5. Merge PR → Create GitHub Release (Automatic)
   ↓
6. Build Python Package (Automatic - triggered by release)
   ↓
7. Publish to PyPI (Automatic - triggered by build)
```

## Workflow Overview

| Workflow | Purpose | Trigger | Documentation |
| --- | --- | --- | --- |
| `start-release-branch.yml` | Create `release/v*` branch and bump prerelease version in `pyproject.toml` | Manual (`workflow_dispatch`) | [start-release-branch.md](start-release-branch.md) |
| `create-github-release.yml` | Create GitHub release after merge of `release/v*` into `main` | Pull request closed+merged into `main` | [create-github-release.md](create-github-release.md) |
| `build-package.yml` | Build wheel + sdist and upload assets/artifacts | Release created or manual (`workflow_dispatch`) | [build-package.md](build-package.md) |
| `generate-lazydocs.yml` | Generate API docs from docstrings and commit updates | Push to non-main (`src/**`, workflow file) or manual | [generate-lazydocs.md](generate-lazydocs.md) |
