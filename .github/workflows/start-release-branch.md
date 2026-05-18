# Start Release Branch Workflow

**File:** `start-release-branch.yml`

## Overview

Creates a new release branch from `main` and bumps the project version in `pyproject.toml` to a `-dev.0` prerelease.

Generated branch pattern:

```text
release/vX.Y.Z
```

## Trigger

- Manual (`workflow_dispatch`)

Input:

- `bump_type` (required): `prerelease`, `preminor`, or `premajor`

## Version Rules

Starting from current project version (base semantic version):

- `prerelease`: increments patch (`X.Y.Z -> X.Y.(Z+1)-dev.0`)
- `preminor`: increments minor (`X.Y.Z -> X.(Y+1).0-dev.0`)
- `premajor`: increments major (`X.Y.Z -> (X+1).0.0-dev.0`)

Branch name always uses the base version without `-dev.0`.

Example:

- New version: `0.2.0-dev.0`
- Branch: `release/v0.2.0`

## What the Workflow Does

1. Checks out `main`.
2. Sets up Python 3.11.
3. Updates `version = "..."` in `pyproject.toml`.
4. Creates and switches to `release/vX.Y.Z`.
5. Commits `pyproject.toml` with message `start release branch`.
6. Pushes the new branch.

## Running It

### GitHub UI

1. Open Actions.
2. Select `Start Release Branch`.
3. Click Run workflow.
4. Choose `bump_type`.

### GitHub CLI

```bash
gh workflow run start-release-branch.yml -f bump_type=prerelease
```

## Troubleshooting

### Commit failed due to no changes

- Verify current `pyproject.toml` version is parseable semantic version.

### Push failed

- Verify workflow token has push permission.
- Verify branch protection rules allow workflow pushes.

## Related Workflows

- Next: [create-github-release.md](create-github-release.md)
- Build step after release: [build-package.md](build-package.md)
