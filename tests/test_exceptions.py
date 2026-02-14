"""Tests for nestdict._exceptions — custom exception hierarchy."""

import pytest

from nestdict._exceptions import (
    FrozenPathError,
    NestDictError,
    PathError,
    PathNotFoundError,
    ValidationError,
)


class TestExceptionHierarchy:
    def test_path_error_is_nestdict_error(self) -> None:
        assert issubclass(PathError, NestDictError)

    def test_path_not_found_is_key_error(self) -> None:
        assert issubclass(PathNotFoundError, KeyError)
        assert issubclass(PathNotFoundError, NestDictError)

    def test_frozen_path_is_type_error(self) -> None:
        assert issubclass(FrozenPathError, TypeError)
        assert issubclass(FrozenPathError, NestDictError)

    def test_validation_error_is_value_error(self) -> None:
        assert issubclass(ValidationError, ValueError)
        assert issubclass(ValidationError, NestDictError)


class TestPathError:
    def test_message(self) -> None:
        err = PathError("bad..path")
        assert "bad..path" in str(err)
        assert err.path == "bad..path"

    def test_custom_message(self) -> None:
        err = PathError("x", "custom message")
        assert "custom message" in str(err)


class TestPathNotFoundError:
    def test_message(self) -> None:
        err = PathNotFoundError("user.email")
        assert "user.email" in str(err)
        assert err.path == "user.email"

    def test_catchable_as_key_error(self) -> None:
        with pytest.raises(KeyError):
            raise PathNotFoundError("user.email")


class TestValidationError:
    def test_message(self) -> None:
        err = ValidationError("user.age", "int", "str", "thirty")
        assert "user.age" in str(err)
        assert "int" in str(err)
        assert "str" in str(err)
        assert err.path == "user.age"
        assert err.expected == "int"
        assert err.got == "str"
        assert err.value == "thirty"

    def test_catchable_as_value_error(self) -> None:
        with pytest.raises(ValueError):
            raise ValidationError("x", "int", "str")


class TestFrozenPathError:
    def test_message(self) -> None:
        err = FrozenPathError("config.db")
        assert "config.db" in str(err)
        assert err.path == "config.db"

    def test_catchable_as_type_error(self) -> None:
        with pytest.raises(TypeError):
            raise FrozenPathError("config.db")
