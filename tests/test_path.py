"""Tests for nestdict._path — path parsing and navigation."""

import pytest

from nestdict._exceptions import PathError, PathNotFoundError
from nestdict._path import (
    PathSegment,
    SegmentKind,
    delete_at,
    exists,
    leaf_paths,
    navigate,
    parse_path,
    segments_to_path,
    set_at,
)

# ── parse_path ──────────────────────────────────────────────────────────


class TestParsePath:
    def test_simple_key(self) -> None:
        result = parse_path("name")
        assert result == [PathSegment(SegmentKind.KEY, "name")]

    def test_dotted_path(self) -> None:
        result = parse_path("user.address.city")
        assert result == [
            PathSegment(SegmentKind.KEY, "user"),
            PathSegment(SegmentKind.KEY, "address"),
            PathSegment(SegmentKind.KEY, "city"),
        ]

    def test_index_segment(self) -> None:
        result = parse_path("items.[0].name")
        assert result == [
            PathSegment(SegmentKind.KEY, "items"),
            PathSegment(SegmentKind.INDEX, 0),
            PathSegment(SegmentKind.KEY, "name"),
        ]

    def test_negative_index(self) -> None:
        result = parse_path("items.[-1]")
        assert result == [
            PathSegment(SegmentKind.KEY, "items"),
            PathSegment(SegmentKind.INDEX, -1),
        ]

    def test_root_index(self) -> None:
        result = parse_path("[0].name")
        assert result == [
            PathSegment(SegmentKind.INDEX, 0),
            PathSegment(SegmentKind.KEY, "name"),
        ]

    def test_multiple_indices(self) -> None:
        result = parse_path("[0].[1].[2]")
        assert result == [
            PathSegment(SegmentKind.INDEX, 0),
            PathSegment(SegmentKind.INDEX, 1),
            PathSegment(SegmentKind.INDEX, 2),
        ]

    def test_empty_path_raises(self) -> None:
        with pytest.raises(PathError):
            parse_path("")

    def test_whitespace_only_raises(self) -> None:
        with pytest.raises(PathError):
            parse_path("   ")

    def test_double_dot_raises(self) -> None:
        with pytest.raises(PathError):
            parse_path("user..name")

    def test_trailing_dot_raises(self) -> None:
        with pytest.raises(PathError):
            parse_path("user.name.")

    def test_leading_dot_raises(self) -> None:
        with pytest.raises(PathError):
            parse_path(".user.name")

    def test_key_with_numbers(self) -> None:
        result = parse_path("item2.value3")
        assert result == [
            PathSegment(SegmentKind.KEY, "item2"),
            PathSegment(SegmentKind.KEY, "value3"),
        ]

    def test_key_with_underscores(self) -> None:
        result = parse_path("my_key.another_key")
        assert result == [
            PathSegment(SegmentKind.KEY, "my_key"),
            PathSegment(SegmentKind.KEY, "another_key"),
        ]

    def test_key_with_hyphens(self) -> None:
        result = parse_path("my-key.another-key")
        assert result == [
            PathSegment(SegmentKind.KEY, "my-key"),
            PathSegment(SegmentKind.KEY, "another-key"),
        ]


# ── segments_to_path ───────────────────────────────────────────────────


class TestSegmentsToPath:
    def test_roundtrip_simple(self) -> None:
        path = "user.address.city"
        assert segments_to_path(parse_path(path)) == path

    def test_roundtrip_with_indices(self) -> None:
        path = "items.[0].name"
        assert segments_to_path(parse_path(path)) == path

    def test_roundtrip_root_index(self) -> None:
        path = "[0].name"
        assert segments_to_path(parse_path(path)) == path


# ── navigate ───────────────────────────────────────────────────────────


class TestNavigate:
    def test_simple_key(self) -> None:
        data = {"name": "Alice"}
        assert navigate(data, "name") == "Alice"

    def test_nested_key(self) -> None:
        data = {"user": {"address": {"city": "NYC"}}}
        assert navigate(data, "user.address.city") == "NYC"

    def test_list_index(self) -> None:
        data = {"items": [10, 20, 30]}
        assert navigate(data, "items.[1]") == 20

    def test_negative_index(self) -> None:
        data = {"items": [10, 20, 30]}
        assert navigate(data, "items.[-1]") == 30

    def test_root_list(self) -> None:
        data = [{"name": "Alice"}, {"name": "Bob"}]
        assert navigate(data, "[1].name") == "Bob"

    def test_nested_list(self) -> None:
        data = {"matrix": [[1, 2], [3, 4]]}
        assert navigate(data, "matrix.[1].[0]") == 3

    def test_dict_value(self) -> None:
        data = {"user": {"address": {"city": "NYC", "zip": "10001"}}}
        result = navigate(data, "user.address")
        assert result == {"city": "NYC", "zip": "10001"}

    def test_missing_key_raises(self) -> None:
        data = {"user": {"name": "Alice"}}
        with pytest.raises(PathNotFoundError):
            navigate(data, "user.email")

    def test_missing_nested_key_raises(self) -> None:
        data = {"user": {"name": "Alice"}}
        with pytest.raises(PathNotFoundError):
            navigate(data, "user.address.city")

    def test_index_on_dict_raises(self) -> None:
        data = {"user": {"name": "Alice"}}
        with pytest.raises(PathNotFoundError):
            navigate(data, "user.[0]")

    def test_key_on_list_raises(self) -> None:
        data = [1, 2, 3]
        with pytest.raises(PathNotFoundError):
            navigate(data, "name")

    def test_index_out_of_range_raises(self) -> None:
        data = {"items": [1, 2]}
        with pytest.raises(PathNotFoundError):
            navigate(data, "items.[5]")

    def test_none_value(self) -> None:
        data = {"value": None}
        assert navigate(data, "value") is None

    def test_zero_value(self) -> None:
        data = {"count": 0}
        assert navigate(data, "count") == 0

    def test_empty_string_value(self) -> None:
        data = {"name": ""}
        assert navigate(data, "name") == ""

    def test_false_value(self) -> None:
        data = {"active": False}
        assert navigate(data, "active") is False

    def test_empty_list_value(self) -> None:
        data = {"items": []}
        assert navigate(data, "items") == []

    def test_empty_dict_value(self) -> None:
        data = {"meta": {}}
        assert navigate(data, "meta") == {}

    def test_index_segment_on_dict_falls_back_to_key(self) -> None:
        """Dict keys that look like indices should be accessible."""
        data = {"items": {"[0]": "first", "[1]": "second"}}
        assert navigate(data, "items.[0]") == "first"
        assert navigate(data, "items.[1]") == "second"

    def test_index_on_list_still_works_after_fallback(self) -> None:
        """Normal list indexing is unaffected by the dict fallback."""
        data = {"items": ["a", "b", "c"]}
        assert navigate(data, "items.[0]") == "a"
        assert navigate(data, "items.[2]") == "c"

    def test_index_on_dict_missing_key_raises(self) -> None:
        """Dict without the literal index key should still raise."""
        data = {"items": {"name": "test"}}
        with pytest.raises(PathNotFoundError):
            navigate(data, "items.[0]")


# ── exists ─────────────────────────────────────────────────────────────


class TestExists:
    def test_existing_path(self) -> None:
        data = {"user": {"name": "Alice"}}
        assert exists(data, "user.name") is True

    def test_missing_path(self) -> None:
        data = {"user": {"name": "Alice"}}
        assert exists(data, "user.email") is False

    def test_partial_path(self) -> None:
        data = {"user": {"name": "Alice"}}
        assert exists(data, "user") is True

    def test_none_value_exists(self) -> None:
        data = {"key": None}
        assert exists(data, "key") is True


# ── set_at ─────────────────────────────────────────────────────────────


class TestSetAt:
    def test_set_existing_key(self) -> None:
        data = {"name": "Alice"}
        set_at(data, "name", "Bob")
        assert data["name"] == "Bob"

    def test_set_nested_key(self) -> None:
        data = {"user": {"name": "Alice"}}
        set_at(data, "user.name", "Bob")
        assert data["user"]["name"] == "Bob"

    def test_create_intermediate_dicts(self) -> None:
        data: dict = {}
        set_at(data, "user.address.city", "NYC")
        assert data == {"user": {"address": {"city": "NYC"}}}

    def test_create_intermediate_for_list(self) -> None:
        data: dict = {}
        set_at(data, "items.[0]", "first")
        assert data == {"items": ["first"]}

    def test_set_in_list(self) -> None:
        data = {"items": [1, 2, 3]}
        set_at(data, "items.[1]", 99)
        assert data["items"][1] == 99

    def test_extend_list(self) -> None:
        data = {"items": [1]}
        set_at(data, "items.[2]", 3)
        assert data["items"] == [1, None, 3]

    def test_set_nested_in_list(self) -> None:
        data = [{"name": "Alice"}]
        set_at(data, "[0].name", "Bob")
        assert data[0]["name"] == "Bob"

    def test_set_index_on_dict(self) -> None:
        """Setting an index segment on a dict uses the literal key."""
        data: dict = {"items": {"[0]": "old"}}
        set_at(data, "items.[0]", "new")
        assert data["items"]["[0]"] == "new"

    def test_set_index_on_dict_creates_key(self) -> None:
        """Setting an index segment on a dict creates the literal key if missing."""
        data: dict = {"items": {"name": "test"}}
        set_at(data, "items.[0]", "value")
        assert data["items"]["[0]"] == "value"
        assert data["items"]["name"] == "test"


# ── delete_at ──────────────────────────────────────────────────────────


class TestDeleteAt:
    def test_delete_key(self) -> None:
        data = {"name": "Alice", "age": 30}
        deleted = delete_at(data, "name")
        assert deleted == "Alice"
        assert data == {"age": 30}

    def test_delete_nested_key(self) -> None:
        data = {"user": {"name": "Alice", "age": 30}}
        deleted = delete_at(data, "user.name")
        assert deleted == "Alice"
        assert data == {"user": {"age": 30}}

    def test_delete_list_item(self) -> None:
        data = {"items": [1, 2, 3]}
        deleted = delete_at(data, "items.[1]")
        assert deleted == 2
        assert data == {"items": [1, 3]}

    def test_delete_missing_raises(self) -> None:
        data = {"name": "Alice"}
        with pytest.raises(PathNotFoundError):
            delete_at(data, "email")

    def test_delete_from_root_list(self) -> None:
        data = [1, 2, 3]
        deleted = delete_at(data, "[0]")
        assert deleted == 1
        assert data == [2, 3]

    def test_delete_index_on_dict(self) -> None:
        """Deleting an index segment on a dict removes the literal key."""
        data: dict = {"items": {"[0]": "val", "other": 1}}
        deleted = delete_at(data, "items.[0]")
        assert deleted == "val"
        assert data == {"items": {"other": 1}}

    def test_delete_index_on_dict_missing_raises(self) -> None:
        """Deleting a missing literal index key from a dict raises."""
        data: dict = {"items": {"name": "test"}}
        with pytest.raises(PathNotFoundError):
            delete_at(data, "items.[0]")


# ── leaf_paths ─────────────────────────────────────────────────────────


class TestLeafPaths:
    def test_flat_dict(self) -> None:
        data = {"a": 1, "b": 2}
        assert sorted(leaf_paths(data)) == ["a", "b"]

    def test_nested_dict(self) -> None:
        data = {"user": {"name": "Alice", "age": 30}}
        assert sorted(leaf_paths(data)) == ["user.age", "user.name"]

    def test_list_paths(self) -> None:
        data = {"items": [10, 20]}
        assert leaf_paths(data) == ["items.[0]", "items.[1]"]

    def test_root_list(self) -> None:
        data = [{"name": "Alice"}, {"name": "Bob"}]
        assert leaf_paths(data) == ["[0].name", "[1].name"]

    def test_empty_dict(self) -> None:
        assert leaf_paths({}) == []

    def test_deeply_nested(self) -> None:
        data = {"a": {"b": {"c": {"d": 1}}}}
        assert leaf_paths(data) == ["a.b.c.d"]

    def test_mixed_types(self) -> None:
        data = {"name": "Alice", "tags": ["python", "dev"], "meta": {"x": 1}}
        result = leaf_paths(data)
        assert "name" in result
        assert "tags.[0]" in result
        assert "tags.[1]" in result
        assert "meta.x" in result
