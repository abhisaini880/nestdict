# nestdict

**The Swiss Army knife for nested Python dicts.**

Access, query, transform, and validate nested data — no schemas, no DSLs, just Python.

> *Pydantic is for data you define. nestdict is for data that arrives.*

![PyPI](https://img.shields.io/pypi/v/nestdict) ![Python](https://img.shields.io/badge/python-3.9%2B-blue) ![Tests](https://img.shields.io/badge/tests-174%20passed-green) ![Coverage](https://img.shields.io/badge/coverage-91%25-brightgreen)

## The Problem

Working with nested dicts in Python is painful:

```python
# The .get().get().get() chain of sadness
city = response.get("data", {}).get("customer", {}).get("address", {}).get("city")

# Or the try/except dance
try:
    city = response["data"]["customer"]["address"]["city"]
except (KeyError, TypeError):
    city = None
```

## The Solution

```python
from nestdict import NestDict

nd = NestDict(api_response)
city = nd.get("data.customer.address.city")  # Done. Returns None if missing.
```

## Installation

```bash
pip install nestdict==2.0.0a1 --pre
```

## Quick Start

```python
from nestdict import NestDict

# Wrap any nested dict or list
data = {
    "user": {
        "name": "Alice",
        "age": 30,
        "address": {"city": "New York", "zip": "10001"}
    },
    "tags": ["developer", "python"]
}

nd = NestDict(data)

# Access with dot paths
nd["user.name"]                  # 'Alice'
nd["user.address.city"]          # 'New York'
nd["tags.[0]"]                   # 'developer'

# Safe access with defaults
nd.get("user.phone")             # None
nd.get("user.phone", "N/A")     # 'N/A'

# Set values (creates intermediates automatically)
nd["user.email"] = "alice@example.com"
nd["settings.theme"] = "dark"    # Creates 'settings' dict automatically

# Delete values
del nd["user.address.zip"]

# Check existence
"user.name" in nd                # True
"user.phone" in nd               # False

# Get multiple values at once
nd.values_at("user.name", "user.age", "user.phone")
# ['Alice', 30, None]

# Export back to plain dict
plain = nd.to_dict()

# Flatten to dot-notation keys
nd.flatten()
# {'user.name': 'Alice', 'user.age': 30, 'user.address.city': 'New York', ...}

# List all leaf paths
nd.paths()
# ['user.name', 'user.age', 'user.address.city', 'user.email', ...]
```

## Functional API

For one-shot operations, use the functional API — no need to create a NestDict:

```python
from nestdict import get, set_at, delete_at, flatten, unflatten, paths, exists

# Direct access on plain dicts
city = get(api_response, "data.customer.address.city")
exists(config, "database.host")  # True/False

# Immutable transforms (returns new dict, original unchanged)
updated = set_at(config, "database.port", 5433)
cleaned = delete_at(user_data, "password")

# Flatten/unflatten
flat = flatten({"a": {"b": 1, "c": 2}})
# {'a.b': 1, 'a.c': 2}

nested = unflatten({"a.b": 1, "a.c": 2})
# {'a': {'b': 1, 'c': 2}}

# All leaf paths
paths(data)
# ['user.name', 'user.age', 'user.address.city', ...]
```

## Works Like a Dict

NestDict implements `collections.abc.MutableMapping`, so it works everywhere a dict does:

```python
nd = NestDict({"x": 1, "y": 2})

len(nd)              # 2
list(nd)             # ['x', 'y']
dict(nd)             # {'x': 1, 'y': 2}
bool(nd)             # True

# Merge with | operator (Python 3.9+)
merged = nd | {"z": 3}
nd |= {"z": 3}

# Copy
import copy
shallow = copy.copy(nd)
deep = copy.deepcopy(nd)
```

## List Support

Works with lists at any level, including as the root:

```python
# Root list
nd = NestDict([{"name": "Alice"}, {"name": "Bob"}])
nd["[0].name"]       # 'Alice'
nd["[1].name"]       # 'Bob'

# Nested lists
data = {"matrix": [[1, 2], [3, 4]]}
nd = NestDict(data)
nd["matrix.[1].[0]"]  # 3

# Negative indices
nd["matrix.[-1].[-1]"]  # 4
```

## Path Syntax

| Pattern | Meaning | Example |
|---------|---------|---------|
| `key` | Dict key | `"name"` |
| `key1.key2` | Nested dict keys | `"user.address.city"` |
| `[n]` | List index | `"[0]"`, `"[-1]"` |
| `key.[n]` | List in dict | `"items.[0].name"` |

## Error Handling

Clear, actionable error messages:

```python
from nestdict import NestDict, PathNotFoundError

nd = NestDict({"user": {"name": "Alice"}})

try:
    nd["user.address.city"]
except PathNotFoundError as e:
    print(e)
    # Path not found: 'user.address.city' — key 'address' does not exist at user
```

Exception hierarchy:
- `NestDictError` — base for all nestdict errors
- `PathError` — malformed path syntax
- `PathNotFoundError` (also a `KeyError`) — path doesn't exist
- `ValidationError` (also a `ValueError`) — validation failure
- `FrozenPathError` (also a `TypeError`) — frozen path mutation

## Roadmap

nestdict v2 is a complete rewrite. Here's what's coming:

- **v2.0.0a1** (current): Core CRUD, flatten/unflatten, functional API
- **v2.0.0a2**: Wildcard queries (`users.*.email`, `**.name`), pick/omit
- **v2.0.0a3**: Deep merge with strategies, structural diff
- **v2.0.0b1**: Validation, frozen paths, schema inference, serialization
- **v2.0.0**: Stable release

## Why Not...?

| Library | What it does | What nestdict adds |
|---------|-------------|-------------------|
| **Pydantic** | Schema-first validation | nestdict works without defining models — for data that arrives |
| **python-box** | Dot attribute access | nestdict adds flatten, paths, functional API, and (coming) query/merge/diff |
| **glom** | Spec-based transforms | nestdict uses simple dot-path strings, not a DSL |
| **jmespath** | JSON query language | nestdict reads AND writes — not just queries |

## Development

```bash
# Clone and install
git clone https://github.com/abhisaini880/nestdict.git
cd nestdict
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# Run tests
pytest --cov=nestdict

# Lint and type check
ruff check nestdict/ tests/
mypy nestdict/
```

## License

MIT License. See [LICENSE](LICENSE) for details.
