# Publish to PyPI Workflow

**File:** `publish-pypi.yml`

## Overview

Publishes the Python package to PyPI after the release workflow has completed successfully.

The workflow downloads wheel + source distribution assets from the GitHub release and uploads exactly those files to PyPI.

## Triggers

- Automatic: `workflow_run` after `Build Python Package` or `Create GitHub Release` completes
- Automatic runs are gated to execute only when the triggering workflow succeeded and is release-related
- Manual: `workflow_dispatch`

Manual input:

- `tag_name` (optional): release tag to publish (for example `v0.2.6`)

## Required Secret

- `PYPI_API_TOKEN`: PyPI API token stored in GitHub repository secrets

## What It Does

1. Determines the release tag from workflow context (`release/vX.Y.Z` branch or `vX.Y.Z` tag), or from manual `tag_name` input.
2. Downloads `.whl` and `.tar.gz` assets from that release into `dist/`.
3. Verifies both files are present.
4. Publishes `dist/*` to PyPI.

## Permissions

- `contents: read`

## Troubleshooting

### Publish workflow did not start

- Verify `Create GitHub Release` workflow run completed successfully.
- Verify this workflow file exists on the default branch.

### Publish failed with authentication errors

- Verify `PYPI_API_TOKEN` is set in repository secrets.
- Verify the token has permission to upload to the target PyPI project.

### Publish failed to determine or download release assets

- For manual runs, provide `tag_name`.
- Verify the referenced release exists.
- Verify the release contains `.whl` and `.tar.gz` assets.

### Publish failed because version already exists

- PyPI does not allow overwriting an existing version.
- Bump the package version and create a new release.
