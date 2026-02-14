"""Tests for nestdict._functional — standalone function API."""

import pytest

from nestdict import (
    delete_at,
    exists,
    flatten,
    get,
    paths,
    set_at,
    unflatten,
)
from nestdict._exceptions import PathNotFoundError

SAMPLE = {"user": {"name": "Alice", "age": 30}, "tags": ["dev", "python"]}


class TestGet:
    def test_existing(self) -> None:
        assert get(SAMPLE, "user.name") == "Alice"

    def test_missing_returns_default(self) -> None:
        assert get(SAMPLE, "user.email") is None

    def test_custom_default(self) -> None:
        assert get(SAMPLE, "user.email", "N/A") == "N/A"

    def test_nested(self) -> None:
        assert get(SAMPLE, "user.age") == 30

    def test_list_index(self) -> None:
        assert get(SAMPLE, "tags.[0]") == "dev"

    def test_falsy_values_returned(self) -> None:
        data = {"zero": 0, "empty": "", "false": False}
        assert get(data, "zero") == 0
        assert get(data, "empty") == ""
        assert get(data, "false") is False


class TestSetAt:
    def test_set_returns_new_copy(self) -> None:
        result = set_at(SAMPLE, "user.name", "Bob")
        assert result["user"]["name"] == "Bob"
        # Original unchanged
        assert SAMPLE["user"]["name"] == "Alice"

    def test_create_new_path(self) -> None:
        result = set_at(SAMPLE, "user.email", "alice@example.com")
        assert result["user"]["email"] == "alice@example.com"

    def test_create_deep_path(self) -> None:
        result = set_at({}, "a.b.c", 1)
        assert result == {"a": {"b": {"c": 1}}}


class TestDeleteAt:
    def test_delete_returns_new_copy(self) -> None:
        result = delete_at(SAMPLE, "user.age")
        assert "age" not in result["user"]
        # Original unchanged
        assert SAMPLE["user"]["age"] == 30

    def test_delete_missing_raises(self) -> None:
        with pytest.raises(PathNotFoundError):
            delete_at(SAMPLE, "user.nonexistent")


class TestExists:
    def test_existing(self) -> None:
        assert exists(SAMPLE, "user.name") is True

    def test_missing(self) -> None:
        assert exists(SAMPLE, "user.email") is False

    def test_partial_path(self) -> None:
        assert exists(SAMPLE, "user") is True


class TestFlatten:
    def test_basic(self) -> None:
        result = flatten({"a": {"b": 1}})
        assert result == {"a.b": 1}


class TestUnflatten:
    def test_basic(self) -> None:
        result = unflatten({"a.b": 1})
        assert result == {"a": {"b": 1}}


class TestPaths:
    def test_basic(self) -> None:
        result = paths({"a": 1, "b": {"c": 2}})
        assert sorted(result) == ["a", "b.c"]

    def test_list(self) -> None:
        result = paths({"items": [1, 2]})
        assert result == ["items.[0]", "items.[1]"]
