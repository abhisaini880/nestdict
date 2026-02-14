"""Tests for nestdict._core — NestDict class."""

import copy

import pytest

from nestdict import NestDict
from nestdict._exceptions import PathNotFoundError

# ── Sample data ────────────────────────────────────────────────────────

SAMPLE_DATA = {
    "user": {
        "name": "Alice",
        "age": 30,
        "address": {"city": "Wonderland", "zip": 12345},
    },
    "preferences": {
        "language": ["English", "French"],
        "timezone": "UTC",
    },
}


# ── Construction ───────────────────────────────────────────────────────


class TestConstruction:
    def test_from_dict(self) -> None:
        nd = NestDict({"a": 1})
        assert nd["a"] == 1

    def test_from_none(self) -> None:
        nd = NestDict()
        assert len(nd) == 0

    def test_from_list(self) -> None:
        nd = NestDict([1, 2, 3])
        assert nd["[0]"] == 1

    def test_from_nestdict(self) -> None:
        original = NestDict({"a": 1})
        copied = NestDict(original)
        assert copied["a"] == 1
        # Verify independence
        copied["a"] = 2
        assert original["a"] == 1

    def test_deep_copy_on_init(self) -> None:
        data = {"user": {"name": "Alice"}}
        nd = NestDict(data)
        nd["user.name"] = "Bob"
        # Original should be unchanged
        assert data["user"]["name"] == "Alice"

    def test_invalid_type_raises(self) -> None:
        with pytest.raises(TypeError, match="NestDict expects"):
            NestDict("not a dict")  # type: ignore[arg-type]

    def test_from_empty_dict(self) -> None:
        nd = NestDict({})
        assert len(nd) == 0
        assert nd.to_dict() == {}


# ── Get / __getitem__ ─────────────────────────────────────────────────


class TestGet:
    def test_get_simple(self) -> None:
        nd = NestDict(SAMPLE_DATA)
        assert nd["user.name"] == "Alice"

    def test_get_deeply_nested(self) -> None:
        nd = NestDict(SAMPLE_DATA)
        assert nd["user.address.city"] == "Wonderland"

    def test_get_list_item(self) -> None:
        nd = NestDict(SAMPLE_DATA)
        assert nd["preferences.language.[0]"] == "English"

    def test_get_missing_raises(self) -> None:
        nd = NestDict(SAMPLE_DATA)
        with pytest.raises(PathNotFoundError):
            nd["user.email"]

    def test_get_with_default(self) -> None:
        nd = NestDict(SAMPLE_DATA)
        assert nd.get("user.email", "N/A") == "N/A"

    def test_get_default_none(self) -> None:
        nd = NestDict(SAMPLE_DATA)
        assert nd.get("user.email") is None

    def test_get_existing_returns_value(self) -> None:
        nd = NestDict(SAMPLE_DATA)
        assert nd.get("user.name") == "Alice"

    def test_get_none_value(self) -> None:
        nd = NestDict({"key": None})
        assert nd.get("key") is None
        assert nd["key"] is None

    def test_get_zero_value(self) -> None:
        nd = NestDict({"count": 0})
        assert nd["count"] == 0

    def test_get_false_value(self) -> None:
        nd = NestDict({"active": False})
        assert nd["active"] is False

    def test_get_empty_string_value(self) -> None:
        nd = NestDict({"name": ""})
        assert nd["name"] == ""

    def test_get_subtree(self) -> None:
        nd = NestDict(SAMPLE_DATA)
        address = nd["user.address"]
        assert address == {"city": "Wonderland", "zip": 12345}


# ── Set / __setitem__ ─────────────────────────────────────────────────


class TestSet:
    def test_set_existing(self) -> None:
        nd = NestDict(SAMPLE_DATA)
        nd["user.name"] = "Bob"
        assert nd["user.name"] == "Bob"

    def test_set_new_key(self) -> None:
        nd = NestDict(SAMPLE_DATA)
        nd["user.email"] = "alice@example.com"
        assert nd["user.email"] == "alice@example.com"

    def test_set_creates_intermediates(self) -> None:
        nd = NestDict({})
        nd["a.b.c"] = 1
        assert nd["a.b.c"] == 1
        assert nd.to_dict() == {"a": {"b": {"c": 1}}}

    def test_set_in_list(self) -> None:
        nd = NestDict({"items": [1, 2, 3]})
        nd["items.[1]"] = 99
        assert nd["items.[1]"] == 99

    def test_set_method(self) -> None:
        nd = NestDict({"a": 1})
        nd.set("a", 2)
        assert nd["a"] == 2

    def test_update_paths(self) -> None:
        nd = NestDict({"user": {"name": "Alice"}})
        nd.update_paths({"user.name": "Bob", "user.age": 25})
        assert nd["user.name"] == "Bob"
        assert nd["user.age"] == 25


# ── Delete / __delitem__ ──────────────────────────────────────────────


class TestDelete:
    def test_delete_key(self) -> None:
        nd = NestDict(SAMPLE_DATA)
        del nd["user.address.city"]
        assert "user.address.city" not in nd
        assert nd["user.address"] == {"zip": 12345}

    def test_delete_method(self) -> None:
        nd = NestDict({"a": 1, "b": 2})
        deleted = nd.delete("a")
        assert deleted == 1
        assert "a" not in nd

    def test_delete_missing_raises(self) -> None:
        nd = NestDict(SAMPLE_DATA)
        with pytest.raises(PathNotFoundError):
            del nd["user.nonexistent"]


# ── Contains ──────────────────────────────────────────────────────────


class TestContains:
    def test_existing_path(self) -> None:
        nd = NestDict(SAMPLE_DATA)
        assert "user.name" in nd

    def test_missing_path(self) -> None:
        nd = NestDict(SAMPLE_DATA)
        assert "user.email" not in nd

    def test_top_level_key(self) -> None:
        nd = NestDict(SAMPLE_DATA)
        assert "user" in nd

    def test_non_string_key(self) -> None:
        nd = NestDict(SAMPLE_DATA)
        assert 42 not in nd  # type: ignore[operator]


# ── Iteration ─────────────────────────────────────────────────────────


class TestIteration:
    def test_iter_dict(self) -> None:
        nd = NestDict({"a": 1, "b": 2, "c": 3})
        assert set(nd) == {"a", "b", "c"}

    def test_iter_list(self) -> None:
        nd = NestDict([10, 20, 30])
        assert list(nd) == ["[0]", "[1]", "[2]"]

    def test_len_dict(self) -> None:
        nd = NestDict({"a": 1, "b": 2})
        assert len(nd) == 2

    def test_len_list(self) -> None:
        nd = NestDict([1, 2, 3])
        assert len(nd) == 3

    def test_len_empty(self) -> None:
        nd = NestDict()
        assert len(nd) == 0


# ── Equality ──────────────────────────────────────────────────────────


class TestEquality:
    def test_equal_nestdicts(self) -> None:
        a = NestDict({"x": 1})
        b = NestDict({"x": 1})
        assert a == b

    def test_not_equal_nestdicts(self) -> None:
        a = NestDict({"x": 1})
        b = NestDict({"x": 2})
        assert a != b

    def test_equal_to_dict(self) -> None:
        nd = NestDict({"x": 1})
        assert nd == {"x": 1}

    def test_equal_to_list(self) -> None:
        nd = NestDict([1, 2])
        assert nd == [1, 2]

    def test_not_equal_to_string(self) -> None:
        nd = NestDict({"x": 1})
        assert nd != "not a dict"


# ── Repr / Str / Bool ────────────────────────────────────────────────


class TestRepresentation:
    def test_repr(self) -> None:
        nd = NestDict({"a": 1})
        assert repr(nd) == "NestDict({'a': 1})"

    def test_str(self) -> None:
        nd = NestDict({"a": 1})
        assert str(nd) == "{'a': 1}"

    def test_bool_true(self) -> None:
        nd = NestDict({"a": 1})
        assert bool(nd) is True

    def test_bool_false(self) -> None:
        nd = NestDict({})
        assert bool(nd) is False

    def test_bool_empty_list(self) -> None:
        nd = NestDict([])
        assert bool(nd) is False


# ── Copy ──────────────────────────────────────────────────────────────


class TestCopy:
    def test_copy(self) -> None:
        nd = NestDict({"a": {"b": 1}})
        shallow = copy.copy(nd)
        assert shallow == nd
        # Top-level is different object
        assert shallow is not nd

    def test_deepcopy(self) -> None:
        nd = NestDict({"a": {"b": 1}})
        deep = copy.deepcopy(nd)
        assert deep == nd
        # Modifying deep copy doesn't affect original
        deep["a.b"] = 99
        assert nd["a.b"] == 1


# ── Merge operators (PEP 584) ─────────────────────────────────────────


class TestMergeOperators:
    def test_or_operator(self) -> None:
        a = NestDict({"x": 1})
        b = NestDict({"y": 2})
        result = a | b
        assert result == {"x": 1, "y": 2}
        # Originals unchanged
        assert a == {"x": 1}
        assert b == {"y": 2}

    def test_or_with_dict(self) -> None:
        nd = NestDict({"x": 1})
        result = nd | {"y": 2}
        assert result == {"x": 1, "y": 2}

    def test_or_override(self) -> None:
        a = NestDict({"x": 1, "y": 2})
        b = NestDict({"y": 3, "z": 4})
        result = a | b
        assert result == {"x": 1, "y": 3, "z": 4}

    def test_ior_operator(self) -> None:
        nd = NestDict({"x": 1})
        nd |= {"y": 2}
        assert nd == {"x": 1, "y": 2}

    def test_or_list_raises(self) -> None:
        a = NestDict([1, 2])
        b = NestDict([3, 4])
        with pytest.raises(TypeError):
            a | b


# ── to_dict ───────────────────────────────────────────────────────────


class TestToDict:
    def test_returns_deep_copy(self) -> None:
        nd = NestDict({"a": {"b": 1}})
        result = nd.to_dict()
        result["a"]["b"] = 99
        # NestDict unaffected
        assert nd["a.b"] == 1

    def test_preserves_structure(self) -> None:
        nd = NestDict(SAMPLE_DATA)
        assert nd.to_dict() == SAMPLE_DATA

    def test_list_data(self) -> None:
        data = [{"name": "Alice"}, {"name": "Bob"}]
        nd = NestDict(data)
        assert nd.to_dict() == data


# ── flatten / paths / values_at ──────────────────────────────────────


class TestUtilityMethods:
    def test_flatten(self) -> None:
        nd = NestDict({"a": {"b": 1, "c": 2}})
        assert nd.flatten() == {"a.b": 1, "a.c": 2}

    def test_paths(self) -> None:
        nd = NestDict({"a": {"b": 1}, "c": 2})
        assert sorted(nd.paths()) == ["a.b", "c"]

    def test_values_at(self) -> None:
        nd = NestDict(SAMPLE_DATA)
        result = nd.values_at("user.name", "user.age", "user.email")
        assert result == ["Alice", 30, None]

    def test_values_at_empty(self) -> None:
        nd = NestDict({"a": 1})
        assert nd.values_at() == []


# ── Edge cases: index keys in dicts ─────────────────────────────────────


class TestIndexKeyInDict:
    def test_get_index_key_from_dict(self) -> None:
        """Dict keys that look like list indices should be accessible."""
        nd = NestDict({"company": {"[0]": "test", "name": "Corp"}})
        assert nd["company.[0]"] == "test"
        assert nd["company.name"] == "Corp"

    def test_set_index_key_in_dict(self) -> None:
        nd = NestDict({"company": {"[0]": "old"}})
        nd["company.[0]"] = "new"
        assert nd["company.[0]"] == "new"

    def test_delete_index_key_from_dict(self) -> None:
        nd = NestDict({"company": {"[0]": "test", "name": "Corp"}})
        del nd["company.[0]"]
        assert "company.[0]" not in nd
        assert nd["company.name"] == "Corp"

    def test_contains_index_key_in_dict(self) -> None:
        nd = NestDict({"company": {"[0]": "test"}})
        assert "company.[0]" in nd
