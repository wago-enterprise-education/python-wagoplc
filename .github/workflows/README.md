# GitHub Actions Workflows

This directory contains automated workflows for building, testing, and deploying the python-wagoplc project.

## Workflow Overview

| Workflow | Purpose | Trigger | Documentation |
| -------- | ------- | ------- | ------------- |
| **lazydocs** | Generate API reference markdown from source code | Push to any branch except main (when src/ changes) or manual trigger | [generate-lazydocs.md](generate-lazydocs.md) |
| **Build Package** | Build pip package (wheel + sdist) with uv | GitHub release published or manual trigger | [build-package.md](build-package.md) |
