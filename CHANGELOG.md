# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Types of changes

All changes should be categorized into one of the following types. These are H3 sections (`###`) below the version headings.

- `Added` for new features.
- `Changed` for changes in existing functionality.
- `Deprecated` for soon-to-be removed features.
- `Removed` for now removed features.
- `Fixed` for any bug fixes.
- `Security` in case of vulnerabilities.

## [Unreleased]

## [0.1.0] - 2026-07-21

### Added

- Initial library structure with `controller`, `tasks`, `read_config`, `constants`, and `exceptions` modules
- `Tasks` class for script-based variable and task registration via decorators (`@tasks.setup`, `@tasks.register`)
- YAML-based configuration (`controller.yaml`) with I/O mapping, state variables, and task definitions
- Schema validation for the `tasks` section in `controller.yaml` using the `schema` library
- Standard library of IEC 61131-3 function blocks: `CTU`, `CTD`, `CTUD`, `TP`, `TON`, `TOF`, `RS`, `SR`, `R_TRIG`, `F_TRIG`
- Support for user-defined function blocks via module-qualified names in config
- CC100 controller implementations: 751-9301, 751-9401, 751-9403
- Watchdog support for cyclic tasks with configurable timeout and sensitivity
- Unit tests for CC100, `read_config`, `Task`, and `Tasks` classes with CI execution across Python 3.8 to 3.14
- GitHub Actions workflows for unit tests, lazydocs API Markdown generation, package builds, release branch creation, and GitHub release creation
- Public documentation including landing page, getting started guide, user guide, development guide, internals, tests, examples, and API reference
- Example PLC applications and focused code examples for traffic lights, conveyor belts, bottle filling, gate control, Arduino-style usage, cycle time handling, and variable mapping
