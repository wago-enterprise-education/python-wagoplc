# Create GitHub Release Workflow

**File:** `create-github-release.yml`

## Overview

Automatically creates a GitHub release when a pull request from `release/v*` to `main` is merged.

The workflow:

1. Extracts the version from branch name `release/vX.Y.Z`.
2. Extracts release notes for that version from `CHANGELOG.md`.
3. Creates release tag `vX.Y.Z` targeting `main`.

After release creation, `build-package.yml` is triggered by the `release` event.

## Trigger Conditions

This workflow runs on pull request close events to `main` and continues only if:

- Pull request is merged.
- Source branch starts with `release/v`.

## Version Detection

Branch format:

```text
release/v1.2.3
```

Detected values:

- Version: `1.2.3`
- Tag: `v1.2.3`

## CHANGELOG Extraction

Expected section format in `CHANGELOG.md`:

```markdown
## [1.2.3] - 2026-05-18
```

Extraction behavior:

- Starts after the exact matching version heading.
- Stops at the next `## [` heading.
- Uses fallback notes if no section exists.

## Required Permissions

- `contents: write` (create release)
- `pull-requests: read` (read PR metadata)

## Troubleshooting

### Workflow did not run

- Verify PR target is `main`.
- Verify source branch starts with `release/v`.
- Verify PR was merged (not only closed).

### Release notes are generic fallback

- Add version section to `CHANGELOG.md` before merging.
- Ensure heading uses exact version in bracket format.

### Release creation failed

- Verify `GITHUB_TOKEN` has repository write access.
- Verify tag does not already exist.

## Related Workflows

- Previous: [start-release-branch.md](start-release-branch.md)
- Next: [build-package.md](build-package.md)
