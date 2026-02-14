"""Standalone functional API for one-shot operations on nested data.

These functions work directly on plain dicts/lists — no need to create
a NestDict instance first.

    from nestdict import get, flatten, paths

    city = get(api_response, "data.customer.address.city")
    flat = flatten(config)
    all_paths = paths(data)
"""

from __future__ import annotations

import copy
from typing import Any

from nestdict._exceptions import PathNotFoundError
from nestdict._flatten import flatten as _flatten_impl
from nestdict._flatten import unflatten as _unflatten_impl
from nestdict._path import (
    delete_at as _delete_at_impl,
)
from nestdict._path import (
    exists as _exists_impl,
)
from nestdict._path import (
    leaf_paths,
    navigate,
)
from nestdict._path import (
    set_at as _set_at_impl,
)


def get(data: Any, path: str, default: Any = None) -> Any:
    """Get a value from nested data by dot-notation path.

    Returns ``default`` if the path does not exist.

    Args:
        data: Nested dict or list.
        path: Dot-notation path string.
        default: Value to return if path is missing.

    Examples:
        >>> get({"a": {"b": 1}}, "a.b")
        1
        >>> get({"a": {"b": 1}}, "a.c", "missing")
        'missing'
    """
    try:
        return navigate(data, path)
    except (PathNotFoundError, KeyError):
        return default


def set_at(data: Any, path: str, value: Any) -> Any:
    """Set a value in nested data by path, returning a new copy.

    The original data is not modified.

    Args:
        data: Nested dict or list.
        path: Dot-notation path string.
        value: Value to set.

    Returns:
        A new deep copy of the data with the value set.

    Examples:
        >>> result = set_at({"a": {"b": 1}}, "a.b", 99)
        >>> result
        {'a': {'b': 99}}
    """
    data_copy = copy.deepcopy(data)
    _set_at_impl(data_copy, path, value)
    return data_copy


def delete_at(data: Any, path: str) -> Any:
    """Delete a value from nested data by path, returning a new copy.

    The original data is not modified.

    Args:
        data: Nested dict or list.
        path: Dot-notation path string.

    Returns:
        A new deep copy of the data with the value removed.

    Raises:
        PathNotFoundError: If the path does not exist.
    """
    data_copy = copy.deepcopy(data)
    _delete_at_impl(data_copy, path)
    return data_copy


def exists(data: Any, path: str) -> bool:
    """Check if a dot-notation path exists in nested data.

    Args:
        data: Nested dict or list.
        path: Dot-notation path string.

    Returns:
        True if the path exists, False otherwise.
    """
    return _exists_impl(data, path)


def flatten(data: Any, separator: str = ".") -> dict[str, Any]:
    """Flatten a nested dict/list into a flat dict with path keys.

    Args:
        data: Nested dict or list.
        separator: Separator between path segments.

    Returns:
        Flat dictionary.

    Examples:
        >>> flatten({"a": {"b": 1, "c": 2}})
        {'a.b': 1, 'a.c': 2}
    """
    return _flatten_impl(data, separator)


def unflatten(flat: dict[str, Any], separator: str = ".") -> Any:
    """Unflatten a flat dict with path keys into a nested structure.

    Args:
        flat: Flat dict with dot-notation keys.
        separator: Separator between path segments.

    Returns:
        Nested dict or list.

    Examples:
        >>> unflatten({"a.b": 1, "a.c": 2})
        {'a': {'b': 1, 'c': 2}}
    """
    return _unflatten_impl(flat, separator)


def paths(data: Any) -> list[str]:
    """Return all leaf paths in a nested data structure.

    Args:
        data: Nested dict or list.

    Returns:
        List of dot-notation path strings.

    Examples:
        >>> paths({"a": {"b": 1}, "c": 2})
        ['a.b', 'c']
    """
    return leaf_paths(data)
