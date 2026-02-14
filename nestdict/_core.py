"""Core NestDict class — a MutableMapping for nested data."""

from __future__ import annotations

import copy
from collections.abc import Iterator, MutableMapping
from typing import Any, overload

from nestdict._exceptions import PathNotFoundError
from nestdict._flatten import flatten as _flatten_data
from nestdict._path import (
    delete_at,
    exists,
    leaf_paths,
    navigate,
    set_at,
)


class NestDict(MutableMapping):  # type: ignore[type-arg]
    """A dict-like container for nested data with dot-path access.

    NestDict wraps a nested dict or list and provides path-based access
    using dot notation. It implements ``collections.abc.MutableMapping``,
    so it works anywhere a dict does: ``len()``, ``in``, ``for``,
    ``dict()``, ``**unpacking``, ``|``, etc.

    Args:
        data: A dict, list, or another NestDict to wrap. Defaults to ``{}``.
            The data is deep-copied on construction to avoid side effects.

    Examples:
        >>> nd = NestDict({"user": {"name": "Alice", "age": 30}})
        >>> nd["user.name"]
        'Alice'
        >>> nd.get("user.phone", "N/A")
        'N/A'
        >>> nd["user.email"] = "alice@example.com"
        >>> del nd["user.age"]
        >>> nd.to_dict()
        {'user': {'name': 'Alice', 'email': 'alice@example.com'}}
    """

    __slots__ = ("_data",)

    def __init__(
        self,
        data: dict[str, Any] | list[Any] | NestDict | None = None,
    ) -> None:
        if data is None:
            self._data: Any = {}
        elif isinstance(data, NestDict):
            self._data = copy.deepcopy(data._data)
        elif isinstance(data, (dict, list)):
            self._data = copy.deepcopy(data)
        else:
            raise TypeError(
                f"NestDict expects dict, list, or NestDict, got {type(data).__name__}"
            )

    # ── MutableMapping interface ──────────────────────────────────────

    def __getitem__(self, path: str) -> Any:
        """Get a value by dot-notation path.

        Raises:
            PathNotFoundError: If the path does not exist.
        """
        return navigate(self._data, path)

    def __setitem__(self, path: str, value: Any) -> None:
        """Set a value by dot-notation path, creating intermediates as needed."""
        set_at(self._data, path, value)

    def __delitem__(self, path: str) -> None:
        """Delete a value by dot-notation path.

        Raises:
            PathNotFoundError: If the path does not exist.
        """
        delete_at(self._data, path)

    def __iter__(self) -> Iterator[str]:
        """Iterate over top-level keys (like a normal dict).

        For all leaf paths, use ``nd.paths()`` instead.
        """
        if isinstance(self._data, dict):
            return iter(self._data)
        elif isinstance(self._data, list):
            return iter(f"[{i}]" for i in range(len(self._data)))
        return iter(())  # pragma: no cover

    def __len__(self) -> int:
        """Return the number of top-level keys/items."""
        return len(self._data)

    # ── get() with default ────────────────────────────────────────────

    @overload
    def get(self, path: str) -> Any: ...

    @overload
    def get(self, path: str, default: Any) -> Any: ...

    def get(self, path: str, default: Any = None) -> Any:
        """Get a value by path, returning ``default`` if not found.

        Unlike ``__getitem__``, this never raises on missing paths.

        Args:
            path: Dot-notation path string.
            default: Value to return if path is missing. Defaults to ``None``.
        """
        try:
            return navigate(self._data, path)
        except (PathNotFoundError, KeyError):
            return default

    # ── Contains / exists ─────────────────────────────────────────────

    def __contains__(self, path: object) -> bool:
        """Check if a dot-notation path exists.

        >>> "user.name" in nd
        True
        """
        if not isinstance(path, str):
            return False
        return exists(self._data, path)

    # ── Equality ──────────────────────────────────────────────────────

    def __eq__(self, other: object) -> bool:
        if isinstance(other, NestDict):
            return bool(self._data == other._data)
        if isinstance(other, (dict, list)):
            return bool(self._data == other)
        return NotImplemented

    # ── Representation ────────────────────────────────────────────────

    def __repr__(self) -> str:
        return f"NestDict({self._data!r})"

    def __str__(self) -> str:
        return str(self._data)

    def __bool__(self) -> bool:
        return bool(self._data)

    # ── Copy support ──────────────────────────────────────────────────

    def __copy__(self) -> NestDict:
        new = NestDict.__new__(NestDict)
        new._data = copy.copy(self._data)
        return new

    def __deepcopy__(self, memo: dict[int, Any] | None = None) -> NestDict:
        new = NestDict.__new__(NestDict)
        new._data = copy.deepcopy(self._data, memo)
        return new

    # ── Merge operators (PEP 584) ─────────────────────────────────────

    def __or__(self, other: dict[str, Any] | NestDict) -> NestDict:
        """Merge two NestDicts (shallow at top level), returning a new one.

        >>> merged = nd1 | nd2
        """
        result = copy.deepcopy(self)
        other_data = other._data if isinstance(other, NestDict) else other
        if isinstance(result._data, dict) and isinstance(other_data, dict):
            result._data.update(copy.deepcopy(other_data))
        else:
            raise TypeError(
                f"Cannot merge {type(self._data).__name__} with "
                f"{type(other_data).__name__} using |"
            )
        return result

    def __ior__(self, other: dict[str, Any] | NestDict) -> NestDict:
        """In-place merge (shallow at top level).

        >>> nd1 |= nd2
        """
        other_data = other._data if isinstance(other, NestDict) else other
        if isinstance(self._data, dict) and isinstance(other_data, dict):
            self._data.update(copy.deepcopy(other_data))
        else:
            raise TypeError(
                f"Cannot merge {type(self._data).__name__} with "
                f"{type(other_data).__name__} using |="
            )
        return self

    # ── Conversion methods ────────────────────────────────────────────

    def to_dict(self) -> Any:
        """Return a deep copy of the underlying data as a plain dict or list.

        The returned object is independent — mutating it won't affect
        the NestDict.
        """
        return copy.deepcopy(self._data)

    def flatten(self, separator: str = ".") -> dict[str, Any]:
        """Return a flat dict with dot-notation path keys.

        Args:
            separator: Separator between path segments.

        Returns:
            Flat dict like ``{"user.name": "Alice", "user.age": 30}``.
        """
        return _flatten_data(self._data, separator)

    def paths(self) -> list[str]:
        """Return all leaf paths in the nested data.

        Returns:
            List of dot-notation path strings.

        >>> nd = NestDict({"a": {"b": 1}, "c": 2})
        >>> nd.paths()
        ['a.b', 'c']
        """
        return leaf_paths(self._data)

    def values_at(self, *path_args: str) -> list[Any]:
        """Retrieve multiple values by path in one call.

        Missing paths return ``None`` (like ``get()``).

        Args:
            *path_args: Dot-notation path strings.

        Returns:
            List of values in the same order as the paths.

        >>> nd.values_at("user.name", "user.age", "user.phone")
        ['Alice', 30, None]
        """
        return [self.get(p) for p in path_args]

    def set(self, path: str, value: Any) -> None:
        """Set a value by path (alias for ``nd[path] = value``).

        Creates intermediate dicts/lists as needed.
        """
        self[path] = value

    def delete(self, path: str) -> Any:
        """Delete a value by path and return it.

        Raises:
            PathNotFoundError: If the path does not exist.
        """
        return delete_at(self._data, path)

    def update_paths(self, mapping: dict[str, Any]) -> None:
        """Set multiple path-value pairs at once.

        Args:
            mapping: Dict of ``{path: value}`` pairs.

        >>> nd.update_paths({"user.name": "Bob", "user.age": 25})
        """
        for path, value in mapping.items():
            self[path] = value
