"""Internal type aliases and sentinel values for nestdict."""

from __future__ import annotations

from typing import Any, Union


class _Missing:
    """Sentinel for distinguishing 'not provided' from None."""

    _instance: _Missing | None = None

    def __new__(cls) -> _Missing:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self) -> str:
        return "<MISSING>"

    def __bool__(self) -> bool:
        return False


MISSING = _Missing()

# Data that NestDict can wrap
NestedData = Union[dict[str, Any], list[Any]]

# A single path segment: either a string key or an integer index
PathSegmentValue = Union[str, int]
