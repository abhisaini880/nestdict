"""Tests for nestdict._flatten — flatten and unflatten operations."""

from nestdict._flatten import flatten, unflatten


class TestFlatten:
    def test_flat_dict_unchanged(self) -> None:
        data = {"a": 1, "b": 2}
        assert flatten(data) == {"a": 1, "b": 2}

    def test_nested_dict(self) -> None:
        data = {"user": {"name": "Alice", "age": 30}}
        result = flatten(data)
        assert result == {"user.name": "Alice", "user.age": 30}

    def test_deeply_nested(self) -> None:
        data = {"a": {"b": {"c": {"d": 1}}}}
        assert flatten(data) == {"a.b.c.d": 1}

    def test_list_values(self) -> None:
        data = {"items": [10, 20, 30]}
        result = flatten(data)
        assert result == {"items.[0]": 10, "items.[1]": 20, "items.[2]": 30}

    def test_nested_list_of_dicts(self) -> None:
        data = {"users": [{"name": "Alice"}, {"name": "Bob"}]}
        result = flatten(data)
        assert result == {"users.[0].name": "Alice", "users.[1].name": "Bob"}

    def test_root_list(self) -> None:
        data = [{"name": "Alice"}, {"name": "Bob"}]
        result = flatten(data)
        assert result == {"[0].name": "Alice", "[1].name": "Bob"}

    def test_empty_dict(self) -> None:
        assert flatten({}) == {}

    def test_empty_nested_dict(self) -> None:
        data = {"meta": {}}
        assert flatten(data) == {"meta": {}}

    def test_empty_list(self) -> None:
        data = {"items": []}
        assert flatten(data) == {"items": []}

    def test_none_values(self) -> None:
        data = {"a": None, "b": {"c": None}}
        result = flatten(data)
        assert result == {"a": None, "b.c": None}

    def test_mixed_types(self) -> None:
        data = {
            "name": "Alice",
            "scores": [95, 87],
            "address": {"city": "NYC"},
        }
        result = flatten(data)
        assert result == {
            "name": "Alice",
            "scores.[0]": 95,
            "scores.[1]": 87,
            "address.city": "NYC",
        }

    def test_custom_separator(self) -> None:
        data = {"a": {"b": 1}}
        result = flatten(data, separator="/")
        assert result == {"a/b": 1}

    def test_nested_lists(self) -> None:
        data = {"matrix": [[1, 2], [3, 4]]}
        result = flatten(data)
        assert result == {
            "matrix.[0].[0]": 1,
            "matrix.[0].[1]": 2,
            "matrix.[1].[0]": 3,
            "matrix.[1].[1]": 4,
        }

    def test_boolean_values(self) -> None:
        data = {"active": True, "deleted": False}
        result = flatten(data)
        assert result == {"active": True, "deleted": False}

    def test_zero_values(self) -> None:
        data = {"count": 0, "nested": {"val": 0}}
        result = flatten(data)
        assert result == {"count": 0, "nested.val": 0}


class TestUnflatten:
    def test_simple(self) -> None:
        flat = {"a.b": 1, "a.c": 2}
        result = unflatten(flat)
        assert result == {"a": {"b": 1, "c": 2}}

    def test_deeply_nested(self) -> None:
        flat = {"a.b.c.d": 1}
        result = unflatten(flat)
        assert result == {"a": {"b": {"c": {"d": 1}}}}

    def test_list_indices(self) -> None:
        flat = {"items.[0]": 10, "items.[1]": 20}
        result = unflatten(flat)
        assert result == {"items": [10, 20]}

    def test_root_list(self) -> None:
        flat = {"[0].name": "Alice", "[1].name": "Bob"}
        result = unflatten(flat)
        assert result == [{"name": "Alice"}, {"name": "Bob"}]

    def test_empty_dict(self) -> None:
        assert unflatten({}) == {}

    def test_flat_dict(self) -> None:
        flat = {"a": 1, "b": 2}
        result = unflatten(flat)
        assert result == {"a": 1, "b": 2}


class TestRoundTrip:
    """Verify that flatten(unflatten(x)) == x and unflatten(flatten(x)) == x."""

    def test_nested_dict_roundtrip(self) -> None:
        data = {"user": {"name": "Alice", "age": 30, "address": {"city": "NYC"}}}
        assert unflatten(flatten(data)) == data

    def test_list_roundtrip(self) -> None:
        data = {"items": [1, 2, 3]}
        assert unflatten(flatten(data)) == data

    def test_root_list_roundtrip(self) -> None:
        data = [{"name": "Alice"}, {"name": "Bob"}]
        assert unflatten(flatten(data)) == data

    def test_complex_roundtrip(self) -> None:
        data = {
            "users": [
                {"name": "Alice", "scores": [95, 87]},
                {"name": "Bob", "scores": [72, 88]},
            ],
            "meta": {"version": 1},
        }
        assert unflatten(flatten(data)) == data
