"""Path parsing and navigation for nested data structures.

This module is the foundation of nestdict. It parses dot-notation path
strings into segments and provides functions to navigate, set, and delete
values in nested dicts/lists.

Path syntax:
    - Dict keys:      "user.address.city"
    - List indices:    "items.[0].name"
    - Negative index:  "items.[-1]"
    - Root list:       "[0].name"
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Any

from nestdict._exceptions import PathError, PathNotFoundError


class SegmentKind(Enum):
    """The type of a path segment."""

    KEY = "key"
    INDEX = "index"


@dataclass(frozen=True)
class PathSegment:
    """A single segment of a parsed path."""

    kind: SegmentKind
    value: str | int

    def __repr__(self) -> str:
        if self.kind == SegmentKind.INDEX:
            return f"[{self.value}]"
        return str(self.value)


# Pre-compiled regex for bracket index segments like [0], [-1]
_INDEX_RE = re.compile(r"^\[(-?\d+)\]$")


def parse_path(path: str) -> list[PathSegment]:
    """Parse a dot-notation path string into a list of PathSegments.

    Args:
        path: A dot-notation path like "user.address.city" or "[0].name"

    Returns:
        List of PathSegment objects.

    Raises:
        PathError: If the path is empty or malformed.

    Examples:
        >>> parse_path("user.name")
        [PathSegment(kind=KEY, value='user'), PathSegment(kind=KEY, value='name')]
        >>> parse_path("items.[0].name")
        [PathSegment(kind=KEY, value='items'), PathSegment(kind=INDEX, value=0), ...]
    """
    if not path or not path.strip():
        raise PathError(path, "Path cannot be empty")

    segments: list[PathSegment] = []
    raw_parts = path.split(".")

    for part in raw_parts:
        if not part:
            raise PathError(path, f"Empty segment in path: {path!r}")

        index_match = _INDEX_RE.match(part)
        if index_match:
            segments.append(
                PathSegment(kind=SegmentKind.INDEX, value=int(index_match.group(1)))
            )
        else:
            segments.append(PathSegment(kind=SegmentKind.KEY, value=part))

    return segments


def segments_to_path(segments: Sequence[PathSegment]) -> str:
    """Convert a list of PathSegments back to a dot-notation path string.

    Args:
        segments: List of PathSegment objects.

    Returns:
        Dot-notation path string.
    """
    parts: list[str] = []
    for seg in segments:
        if seg.kind == SegmentKind.INDEX:
            parts.append(f"[{seg.value}]")
        else:
            parts.append(str(seg.value))
    return ".".join(parts)


def navigate(data: Any, path: str) -> Any:
    """Navigate to a value in nested data using a dot-notation path.

    Args:
        data: The nested dict/list to navigate.
        path: Dot-notation path string.

    Returns:
        The value at the given path.

    Raises:
        PathNotFoundError: If the path does not exist in the data.
        PathError: If the path is malformed.
    """
    segments = parse_path(path)
    return _navigate_segments(data, segments, path)


def _navigate_segments(
    data: Any, segments: list[PathSegment], original_path: str
) -> Any:
    """Internal: navigate using pre-parsed segments."""
    current = data
    traversed: list[PathSegment] = []

    for seg in segments:
        try:
            if seg.kind == SegmentKind.INDEX:
                if isinstance(current, list):
                    current = current[seg.value]  # type: ignore[index]
                elif isinstance(current, dict):
                    # Fallback: try literal "[0]" as a dict key
                    str_key = f"[{seg.value}]"
                    if str_key not in current:
                        loc = segments_to_path(traversed) if traversed else "<root>"
                        raise PathNotFoundError(
                            original_path,
                            f"Path not found: {original_path!r} — key {str_key!r} "
                            f"does not exist at {loc}",
                        )
                    current = current[str_key]
                else:
                    loc = segments_to_path(traversed) if traversed else "<root>"
                    raise PathNotFoundError(
                        original_path,
                        f"Path not found: {original_path!r} — expected list or dict at "
                        f"{loc}, got {type(current).__name__}",
                    )
            else:
                if not isinstance(current, dict):
                    loc = segments_to_path(traversed) if traversed else "<root>"
                    raise PathNotFoundError(
                        original_path,
                        f"Path not found: {original_path!r} — expected dict at "
                        f"{loc}, got {type(current).__name__}",
                    )
                if seg.value not in current:
                    loc = segments_to_path(traversed) if traversed else "<root>"
                    raise PathNotFoundError(
                        original_path,
                        f"Path not found: {original_path!r} — key {seg.value!r} "
                        f"does not exist at {loc}",
                    )
                current = current[seg.value]
        except (IndexError, KeyError) as exc:
            raise PathNotFoundError(
                original_path,
                f"Path not found: {original_path!r}",
            ) from exc

        traversed.append(seg)

    return current


def exists(data: Any, path: str) -> bool:
    """Check if a path exists in nested data.

    Args:
        data: The nested dict/list to check.
        path: Dot-notation path string.

    Returns:
        True if the path exists, False otherwise.
    """
    try:
        navigate(data, path)
        return True
    except (PathNotFoundError, PathError):
        return False


def set_at(data: Any, path: str, value: Any) -> None:
    """Set a value at a path in nested data, creating intermediates as needed.

    Mutates the data in place.

    Args:
        data: The nested dict/list to modify.
        path: Dot-notation path string.
        value: The value to set.

    Raises:
        PathError: If the path is malformed.
        PathNotFoundError: If an intermediate path cannot be navigated
            (e.g., trying to index into a non-list).
    """
    segments = parse_path(path)
    if not segments:
        raise PathError(path, "Cannot set at empty path")

    parent_segments = segments[:-1]
    target_seg = segments[-1]

    # Navigate to the parent, creating intermediates
    current = data
    for i, seg in enumerate(parent_segments):
        next_seg = segments[i + 1]

        if seg.kind == SegmentKind.INDEX:
            if isinstance(current, list):
                # Extend list if needed
                idx = int(seg.value)
                while len(current) <= idx:
                    current.append(None)
                if current[idx] is None:
                    current[idx] = (
                        [] if next_seg.kind == SegmentKind.INDEX else {}
                    )
                current = current[idx]
            elif isinstance(current, dict):
                # Fallback: use literal "[0]" as dict key
                str_key = f"[{seg.value}]"
                if str_key not in current:
                    current[str_key] = (
                        [] if next_seg.kind == SegmentKind.INDEX else {}
                    )
                current = current[str_key]
            else:
                raise PathNotFoundError(
                    path,
                    f"Cannot index into {type(current).__name__} at "
                    f"{segments_to_path(segments[:i]) or '<root>'}",
                )
        else:
            if not isinstance(current, dict):
                raise PathNotFoundError(
                    path,
                    f"Cannot access key on {type(current).__name__} at "
                    f"{segments_to_path(segments[:i]) or '<root>'}",
                )
            if seg.value not in current:
                current[seg.value] = [] if next_seg.kind == SegmentKind.INDEX else {}
            current = current[seg.value]

    # Set the final value
    if target_seg.kind == SegmentKind.INDEX:
        if isinstance(current, list):
            idx = int(target_seg.value)
            while len(current) <= idx:
                current.append(None)
            current[idx] = value
        elif isinstance(current, dict):
            # Fallback: use literal "[0]" as dict key
            str_key = f"[{target_seg.value}]"
            current[str_key] = value
        else:
            raise PathNotFoundError(
                path,
                f"Cannot index into {type(current).__name__} at "
                f"{segments_to_path(parent_segments) or '<root>'}",
            )
    else:
        if not isinstance(current, dict):
            raise PathNotFoundError(
                path,
                f"Cannot set key on {type(current).__name__} at "
                f"{segments_to_path(parent_segments) or '<root>'}",
            )
        current[target_seg.value] = value


def delete_at(data: Any, path: str) -> Any:
    """Delete a value at a path in nested data.

    Mutates the data in place.

    Args:
        data: The nested dict/list to modify.
        path: Dot-notation path string.

    Returns:
        The deleted value.

    Raises:
        PathNotFoundError: If the path does not exist.
        PathError: If the path is malformed.
    """
    segments = parse_path(path)
    if not segments:
        raise PathError(path, "Cannot delete at empty path")

    # Navigate to the parent
    parent_segments = segments[:-1]
    target_seg = segments[-1]

    if parent_segments:
        parent = _navigate_segments(data, parent_segments, path)
    else:
        parent = data

    # Delete the target
    if target_seg.kind == SegmentKind.INDEX:
        if isinstance(parent, list):
            try:
                assert isinstance(target_seg.value, int)
                value = parent[target_seg.value]
                del parent[target_seg.value]
                return value
            except IndexError as exc:
                raise PathNotFoundError(
                    path, f"Index {target_seg.value} out of range"
                ) from exc
        elif isinstance(parent, dict):
            # Fallback: use literal "[0]" as dict key
            str_key = f"[{target_seg.value}]"
            if str_key not in parent:
                raise PathNotFoundError(
                    path,
                    f"Path not found: {path!r} — key {str_key!r} does not exist",
                )
            return parent.pop(str_key)
        else:
            raise PathNotFoundError(
                path,
                f"Cannot index into {type(parent).__name__}",
            )
    else:
        if not isinstance(parent, dict):
            raise PathNotFoundError(
                path,
                f"Cannot delete key from {type(parent).__name__}",
            )
        if target_seg.value not in parent:
            raise PathNotFoundError(
                path,
                f"Path not found: {path!r} — key {target_seg.value!r} does not exist",
            )
        return parent.pop(target_seg.value)


def leaf_paths(data: Any, prefix: str = "") -> list[str]:
    """Return all leaf paths in a nested data structure.

    A leaf is a value that is neither a dict nor a list.

    Args:
        data: The nested dict/list to traverse.
        prefix: Internal prefix for recursion (don't pass this).

    Returns:
        List of dot-notation path strings to all leaf values.
    """
    paths: list[str] = []

    if isinstance(data, dict):
        if not data:
            # Empty dict is a leaf
            if prefix:
                paths.append(prefix)
            return paths
        for key, value in data.items():
            new_path = f"{prefix}.{key}" if prefix else key
            paths.extend(leaf_paths(value, new_path))
    elif isinstance(data, list):
        if not data:
            # Empty list is a leaf
            if prefix:
                paths.append(prefix)
            return paths
        for i, value in enumerate(data):
            new_path = f"{prefix}.[{i}]" if prefix else f"[{i}]"
            paths.extend(leaf_paths(value, new_path))
    else:
        if prefix:
            paths.append(prefix)

    return paths
