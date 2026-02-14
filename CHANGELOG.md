# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
with [PEP 440](https://peps.python.org/pep-0440/) pre-release versioning.

## [2.0.0a1] - Unreleased

### Added
- Complete rewrite with new architecture
- `NestDict` class implementing `collections.abc.MutableMapping`
- Path-based access with dot notation: `nd["user.address.city"]`
- Bracket notation for list indices: `nd["items.[0].name"]`
- `get()`, `set()`, `delete()` methods with clear error messages
- `to_dict()`, `flatten()`, `paths()`, `values_at()` utility methods
- `|` and `|=` merge operators (PEP 584)
- Functional API: `get()`, `set_at()`, `delete_at()`, `flatten()`, `unflatten()`, `paths()`
- Custom exception hierarchy: `PathError`, `PathNotFoundError`, `ValidationError`
- Full type annotations with `py.typed` marker
- `pyproject.toml` based packaging
- GitHub Actions CI for Python 3.9-3.13

### Changed
- Internal storage uses nested dict directly (no parallel flat representation)
- Composition-based design replaces inheritance chain

### Removed
- Old `BaseNestDict`, `ValidationDict`, `FrozenDict` class hierarchy
- Standalone utility functions (`find_in_map`, `all_keys`, `check_keys`, `change_value`)
- `setup.py` (replaced by `pyproject.toml`)

## [1.0.1] - Legacy

The original release. See git history for details.
