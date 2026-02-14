"""Custom exceptions for nestdict."""

from __future__ import annotations


class NestDictError(Exception):
    """Base exception for all nestdict errors."""


class PathError(NestDictError):
    """Raised when a path string is malformed or invalid."""

    def __init__(self, path: str, message: str | None = None) -> None:
        self.path = path
        msg = message or f"Invalid path: {path!r}"
        super().__init__(msg)


class PathNotFoundError(NestDictError, KeyError):
    """Raised when a path does not exist in the data."""

    def __init__(self, path: str, message: str | None = None) -> None:
        self.path = path
        msg = message or f"Path not found: {path!r}"
        # KeyError uses args[0] for its message display
        NestDictError.__init__(self, msg)
        KeyError.__init__(self, msg)


class FrozenPathError(NestDictError, TypeError):
    """Raised when attempting to mutate a frozen path."""

    def __init__(self, path: str) -> None:
        self.path = path
        msg = f"Cannot modify frozen path: {path!r}"
        super().__init__(msg)


class ValidationError(NestDictError, ValueError):
    """Raised when a value fails validation."""

    def __init__(
        self, path: str, expected: str, got: str, value: object = None
    ) -> None:
        self.path = path
        self.expected = expected
        self.got = got
        self.value = value
        msg = f"Validation failed at {path!r}: expected {expected}, got {got}"
        super().__init__(msg)
