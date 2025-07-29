# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2024-05-17

### Added
- Added `owner` parameter to `create_database` function to specify the database owner role

## [1.0.0] - 2024-05-16

### Added
- Initial public release.
- Async context managers: `autocommit`, `switch_role`, `obtain_advisory_lock`.
- Logging connection and cursor classes.
- Query helpers: `create_database`, `database_exists`, `drop_database`.
- Custom exception: `AlreadyExistsError`.
- Top-level API for all helpers, context managers, and exceptions.