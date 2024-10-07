# NestDict: Advanced Nested Dictionary Library for Python

![PyPI](https://img.shields.io/pypi/v/nestdict) ![Python Versions](https://img.shields.io/badge/python-3.6%2B-blue)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)

## Overview

`NestDict` is a powerful Python library that extends the standard dictionary functionality to handle nested dictionaries, providing advanced features such as validation and support for frozen dictionaries. This library simplifies the manipulation of complex data structures, making it an ideal choice for applications that require dynamic data management.

## Features

- **Nested Dictionary Handling**: Seamlessly access and manipulate deeply nested dictionaries.
- **Validation**: Validate data types based on predefined mappings.
- **Frozen Dictionaries**: Create immutable nested dictionaries to protect critical data.
- **List Support**: Manage lists within nested structures effectively.

## Installation

You can install `NestDict` using pip:

``` bash
pip install nestdict
```

## Usage
Here’s a quick example of how to use NestDict:
``` python
from nestdict import NestDict

# Create a nested dictionary
data = {
    "user": {
        "name": "John Doe",
        "age": 30,
        "address": {
            "city": "New York",
            "zip": "10001"
        }
    }
}

# Initialize NestDict
nested_dict = NestDict(data)

# Access nested data
print(nested_dict.get("user.name"))  # Output: John Doe

# Set new values
nested_dict["user.age"] =  31

# print out dict
print(nested_dict)

# save final dict object
final_dict = nested_dict.to_dict()

# Validate data
validation_rules = {
    "user.age": int,
    "user.name": str
}
nested_dict_with_validation = NestDict(data, validation=validation_rules)

```
## API Reference

- `get(key_path, default=None)`
Retrieves the value at the specified key path in the nested dictionary. If the key path does not exist, it returns the specified default value (or `None` if not provided).

- `__getitem__(key_path)`
Allows access to the value at the specified key path using bracket notation (e.g., `nested_dict[key_path]`). Raises a `KeyError` if the key path is not found.

- `__setitem__(key_path, value)`
Sets the value at the specified key path using bracket notation (e.g., `nested_dict[key_path] = value`). It validates the value's type according to the validation rules if provided during initialization.

- `delete(key_path)`
Deletes the value at the specified key path. If the key path does not exist, it raises a `KeyError`.

- `to_dict()`
Returns the nested structure as a standard dictionary, representing the current state of the data.


### Data Parameter

The **data** parameter is the initial nested dictionary structure that you want to manage using the `NestDict` class. It can be any valid Python dictionary (or list of dictionaries) that you need to work with.

#### Key Points:
- **Type**: Accepts a `dict` or `list`.
- **Nested Structure**: You can create deeply nested dictionaries. For example, `{"a": {"b": {"c": 1}}}` is a valid input.
- **Mutable**: The data is mutable, meaning you can modify it using the available methods like `set`, `delete`, or through direct item access.


### Validation Parameter

The **validation** parameter is an optional dictionary used to enforce type checking on the values in your nested dictionary. It allows you to define expected data types for specific keys.

#### Key Points:
- **Type**: Accepts a `dict` where:
  - **Keys**: Are the key paths (in dot notation) that you want to validate. For example, `"user.age"` for a nested dictionary structure.
  - **Values**: Are the expected data types (e.g., `int`, `str`, `list`, `dict`) for those keys.
- **Validation Check**: When you set a value for a key specified in the validation dictionary, the library checks if the value is of the expected type. If it’s not, a `ValueError` is raised.
- **Initialization Validation**: The validation is performed both during the initialization of the `NestDict` instance and when using the `set` method.

## Contributing Guidelines

Contributions to NestDict are welcome! To maintain a high standard for our project, please follow these guidelines when contributing:

1. **Fork the Repository**: Start by forking the repository to your account.

2. **Create a New Branch**: Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature/YourFeatureName
    ```
3. **Make Changes**: Implement your changes and ensure that your code adheres to our coding standards.

4. **Write Tests**: If applicable, add unit tests to cover your changes. Ensure that all tests pass before submitting your changes.

5. **Commit Your Changes**: Use clear and concise commit messages that explain the purpose of the changes. Refer to the COMMIT_GUIDELINES.md for detailed commit message conventions.

6. **Push Your Branch**: Push your changes to your fork:

    ```bash
    git push origin feature/YourFeatureName
    ```
7. **Submit a Pull Request**: Navigate to the original repository and submit a pull request, explaining your changes and the motivation behind them.

8. **Respect the License**: Ensure that any contributions you make do not violate the existing license terms. Contributions should not be commercialized without explicit permission.

*Thank you for contributing to NestDict!*

## Commit Guidelines
We follow specific conventions for our commit messages to maintain clarity and consistency. Please refer to the [COMMIT_GUIDELINES.md](COMMIT_GUIDELINES.md) file for detailed commit message conventions.

## License
This project is licensed under the MIT License. See the [License](LICENSE) file for more details.
