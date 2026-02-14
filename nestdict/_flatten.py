"""Flatten and unflatten nested data structures.

Converts between nested dicts/lists and flat dicts with dot-notation keys.
"""

from __future__ import annotations

from typing import Any


def flatten(data: Any, separator: str = ".") -> dict[str, Any]:
    """Flatten a nested dict/list into a single-level dict with path keys.

    Args:
        data: Nested dict or list to flatten.
        separator: Separator between path segments (default ".").

    Returns:
        Flat dictionary where keys are dot-notation paths.

    Examples:
        >>> flatten({"a": {"b": 1, "c": 2}})
        {"a.b": 1, "a.c": 2}
        >>> flatten({"items": [10, 20]})
        {"items.[0]": 10, "items.[1]": 20}
    """
    result: dict[str, Any] = {}
    _flatten_recursive(data, "", separator, result)
    return result


def _flatten_recursive(
    data: Any, prefix: str, separator: str, result: dict[str, Any]
) -> None:
    """Recursively flatten data into result dict."""
    if isinstance(data, dict):
        if not data:
            # Preserve empty dicts as leaf values
            if prefix:
                result[prefix] = data
            return
        for key, value in data.items():
            new_key = f"{prefix}{separator}{key}" if prefix else key
            _flatten_recursive(value, new_key, separator, result)
    elif isinstance(data, list):
        if not data:
            # Preserve empty lists as leaf values
            if prefix:
                result[prefix] = data
            return
        for i, value in enumerate(data):
            new_key = f"{prefix}{separator}[{i}]" if prefix else f"[{i}]"
            _flatten_recursive(value, new_key, separator, result)
    else:
        if prefix:
            result[prefix] = data
        # If prefix is empty and data is a scalar, there's nothing to flatten


def unflatten(flat: dict[str, Any], separator: str = ".") -> Any:
    """Unflatten a flat dict with path keys back into a nested structure.

    Args:
        flat: Flat dictionary with dot-notation path keys.
        separator: Separator between path segments (default ".").

    Returns:
        Nested dict or list.

    Examples:
        >>> unflatten({"a.b": 1, "a.c": 2})
        {"a": {"b": 1, "c": 2}}
        >>> unflatten({"[0].name": "Alice", "[1].name": "Bob"})
        [{"name": "Alice"}, {"name": "Bob"}]
    """
    if not flat:
        return {}

    # Determine if root is a list or dict
    is_root_list = all(_is_index_segment(k.split(separator)[0]) for k in flat)

    if is_root_list:
        root: Any = []
    else:
        root = {}

    for compound_key, value in flat.items():
        parts = compound_key.split(separator)
        _set_nested(root, parts, value)

    return root


def _is_index_segment(part: str) -> bool:
    """Check if a path segment is a list index like [0] or [-1]."""
    return bool(part.startswith("[") and part.endswith("]"))


def _parse_index(part: str) -> int:
    """Parse a bracket index segment like '[0]' to int."""
    return int(part[1:-1])


def _set_nested(current: Any, parts: list[str], value: Any) -> None:
    """Set a value in a nested structure by walking path parts."""
    for i, part in enumerate(parts[:-1]):
        next_part = parts[i + 1]
        next_is_index = _is_index_segment(next_part)

        if _is_index_segment(part):
            idx = _parse_index(part)
            # Extend list if needed
            while isinstance(current, list) and len(current) <= idx:
                current.append(None)
            if isinstance(current, list):
                if current[idx] is None:
                    current[idx] = [] if next_is_index else {}
                current = current[idx]
        else:
            if isinstance(current, dict):
                if part not in current:
                    current[part] = [] if next_is_index else {}
                current = current[part]

    # Set the final value
    last_part = parts[-1]
    if _is_index_segment(last_part):
        idx = _parse_index(last_part)
        if isinstance(current, list):
            while len(current) <= idx:
                current.append(None)
            current[idx] = value
    else:
        if isinstance(current, dict):
            current[last_part] = value
