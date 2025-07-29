# Baresquare Python Libraries

This monorepo hosts Baresquare's Python packages, all published to PyPI.

## Packages

The repository currently contains the following packages:

- **baresquare_core_py**: Core utilities shared across Baresquare services
- **baresquare_aws_py**: AWS-specific utilities that build upon core

## Development Guidelines

### Versioning

- All packages share the same version number
- Version is defined in each package's `__init__.py` file (`__version__ = "x.y.z"`)
- Git tags must match the version in `__init__.py` files (format: `vx.y.z`)
- CI will validate version consistency before publishing

### Package Configuration

- A single `pyproject.toml` file is used for all packages
- Package-specific settings are handled in the CI process
- Dependencies between packages are defined in `pyproject.toml` under `[project.optional-dependencies]`

### Development Setup

To set up the packages for development:

```shell
# Install in development mode with all dependencies
pip install -e ".[testing]"

# Run tests
pytest
```

### Testing

- Tests are organized by package in the `tests/` directory
- Run tests with pytest
- CI automatically runs tests on all pull requests

## Publishing

Packages are published to PyPI through GitHub Actions when a new tag is pushed:

1. Update version in all `__init__.py` files (must be identical)
1. Commit changes
1. Create and push a tag matching the version (assuming version to be published is 0.1.0):
   - via command line: `git tag v0.1.0 && git push origin v0.1.0`
   - via GitHub UI: Go to "Releases" → "Draft a new release" → "Choose a tag" → Enter "v0.1.0" → "Create new tag"

CI will validate versions, build packages, and publish to PyPI

## Installation


```shell
# Install core package
pip install baresquare_core_py

# Install AWS package (which includes core)
pip install baresquare_aws_py
```

## License

MIT License