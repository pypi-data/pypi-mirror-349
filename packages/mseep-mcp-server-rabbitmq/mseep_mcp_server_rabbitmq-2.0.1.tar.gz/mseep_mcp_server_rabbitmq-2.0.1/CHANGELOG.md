# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2025-05-15

### Added
- Added CONTRIBUTING.md with development guidelines and workflow instructions
- Improved documentation for contributor onboarding

### Changed
- Enhanced error handling for RabbitMQ connection failures
- Updated dependencies to latest versions for improved security
- Use loguru for better logging matainability. Logging to stderr by default.

### Fixed
- Fixed issue with queue name validation in certain edge cases

## [2.0.0] - 2025-04-30

### Added
- Initial release of RabbitMQ MCP Server
- Support for basic queue and exchange operations
- FastMCP integration for improved performance and maintainability
- Ruff linting and formatting configuration
- Testing infrastructure with pytest
