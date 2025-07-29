# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2024-01-17

### ⚠️ BREAKING CHANGES
- Strict mode is now the default for `init` command
- Required fields (name, analyst) must be provided
- Legacy behavior available with `--legacy` flag (will be removed in v0.3.0)

### Added
- User profile system for storing default values
- Smart project name parsing to extract metadata
- Interactive prompts for missing required fields
- Comprehensive validation with clear error messages
- Environment variable support (LDA_ANALYST, LDA_ORGANIZATION, LDA_EMAIL)
- `--strict` and `--legacy` flags for init command
- `profile` command with setup, show, and set subcommands
- Lazy logging to prevent empty log files
- Improved test coverage for new features

### Changed
- `init` command now requires `--name` and `--analyst` by default
- Improved error messages with validation details
- Better documentation for migration from older versions
- Updated all documentation to reflect new strict mode default

### Deprecated
- Legacy init behavior (init without required fields)
- Use `--legacy` flag temporarily, will be removed in v0.3.0

### Fixed
- Status command now correctly displays project metadata from config
- Empty log files are no longer created when no logging occurs

## [0.1.0] - 2024-05-17

### Added
- Initial release of LDA package
- Basic project scaffolding functionality
- File tracking and manifest management
- Command line interface with core commands
- YAML configuration support
- Template system for project initialization
- Basic documentation and examples

### Changed
- Restructured from monolithic script to modular package
- Separated configuration from code
- Improved error handling and validation

### Fixed
- Double "wk" prefix issue in file naming
- Platform compatibility issues