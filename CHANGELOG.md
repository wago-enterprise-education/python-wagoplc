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

### Added

- Initial library structure with `controller`, `tasks`, `read_config`, `constants`, and `exceptions` modules
- `Tasks` class for script-based variable and task registration via decorators (`@tasks.setup`, `@tasks.register`)
- YAML-based configuration (`controller.yaml`) with I/O mapping, state variables, and task definitions
- Schema validation for the `tasks` section in `controller.yaml` using the `schema` library
- Standard library of IEC 61131-3 function blocks: `CTU`, `CTD`, `CTUD`, `TP`, `TON`, `TOF`, `RS`, `SR`, `R_TRIG`, `F_TRIG`
- Support for user-defined function blocks via module-qualified names in config
- CC100 controller implementations: 751-9301, 751-9401, 751-9403
- Watchdog support for cyclic tasks with configurable timeout and sensitivity
- Duplicate I/O mapping detection at startup
- Unit tests for CC100, `read_config`, `Task`, and `Tasks` classes
- GitHub Actions workflow for lazydocs API Markdown generation (`docs/api/`)
- GitHub Actions workflow for building pip package (wheel + sdist) with `uv` on release publish
- Internal workflow diagram (`docs/work_schedule.svg`)
- User guide, development guide, and internals documentation
- Example PLC applications (traffic light, conveyor belt, bottle filling plant, factory gate control)

### Changed

- Moved file descriptor logic into `CC100_v1` class
- Moved configuration parsing into dedicated `read_config` module
- Improved I/O data structures; added `_get_data`/`_set_data` to `Controller` base class
- Simplified task entry-point definition in `controller.yaml`
- Restructured documentation from single README into separate guide files

### Fixed

- Digital output write bug in `CC100_v1`
- `TOF` initialisation (wrong initial `q` value)
- `read_config` not correctly reading the `itemNumber` field in some cases
- Config file not found when running from outside the application directory
- Rising edge detection made consistent across all function blocks
