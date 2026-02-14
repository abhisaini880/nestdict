"""nestdict — The Swiss Army knife for nested Python dicts.

Access, query, transform, and validate nested data — no schemas, no DSLs,
just Python.

    from nestdict import NestDict

    nd = NestDict({"user": {"name": "Alice", "age": 30}})
    nd["user.name"]        # 'Alice'
    nd.get("user.phone")   # None

Functional API for one-shot operations:

    from nestdict import get, flatten, paths

    city = get(api_response, "data.customer.address.city")
    flat = flatten(config)
"""

__version__ = "2.0.0a1"

# Core class
from nestdict._core import NestDict

# Exceptions
from nestdict._exceptions import (
    FrozenPathError,
    NestDictError,
    PathError,
    PathNotFoundError,
    ValidationError,
)

# Functional API
from nestdict._functional import (
    delete_at,
    exists,
    flatten,
    get,
    paths,
    set_at,
    unflatten,
)

__all__ = [
    # Core
    "NestDict",
    # Functional API
    "get",
    "set_at",
    "delete_at",
    "exists",
    "flatten",
    "unflatten",
    "paths",
    # Exceptions
    "NestDictError",
    "PathError",
    "PathNotFoundError",
    "FrozenPathError",
    "ValidationError",
    # Metadata
    "__version__",
]
