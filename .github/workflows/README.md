# GitHub Actions Workflows

This directory contains the CI/CD workflows used by `python-wagoplc`.

## Release Flow

The release automation is organized as follows:

```text
1. Start Release Branch (Manual) 
   ↓
2. Development & Testing on release/v* branch
   ↓
3. Create Pull Request (release/v* → main)
   ↓
4. Merge PR → Create GitHub Release (Automatic)
   ↓
5. Build Python Package (Automatic - called from Create GitHub Release via workflow_call)
   ↓
6. Deploy versioned docs with mike and update `latest` (Automatic - job in Create GitHub Release)
   ↓
7. Publish to PyPI (Automatic - workflow_run after successful release-related Build Python Package or Create GitHub Release)
```

Independently, `docs-deploy-dev.yml` deploys the `dev` documentation version on every push to `main` that touches documentation or source paths.

## Workflow Overview

| Workflow | Purpose | Trigger | Documentation |
| --- | --- | --- | --- |
| `start-release-branch.yml` | Create `release/v*` branch and bump prerelease version in `pyproject.toml` | Manual (`workflow_dispatch`) | [start-release-branch.md](start-release-branch.md) |
| `create-github-release.yml` | Create GitHub release after merge of `release/v*` into `main` | Pull request closed+merged into `main` | [create-github-release.md](create-github-release.md) |
| `build-package.yml` | Build wheel + sdist and upload assets/artifacts | Release created, reusable call (`workflow_call`), or manual (`workflow_dispatch`) | [build-package.md](build-package.md) |
| `publish-pypi.yml` | Publish wheel + sdist to PyPI | `workflow_run` after successful release-related `Build Python Package` or `Create GitHub Release`, or manual (`workflow_dispatch`) | [publish-pypi.md](publish-pypi.md) |
| `docs-deploy-dev.yml` | Build MkDocs site and deploy `dev` docs version with mike | Push to `main` on matching paths (`docs/**`, `src/**`, `mkdocs.yml`, `pyproject.toml`, workflow file), or manual | [docs-deploy-dev.md](docs-deploy-dev.md) |
| `run-tests.yml` | Run the unittest suite and upload JUnit XML results | Push to all branches on matching paths (`src/**`, `tests/**`, `pyproject.toml`, workflow file), or manual | [run-tests.md](run-tests.md) |
