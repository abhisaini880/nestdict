__all__ = ["NestDict"]


from typing import Any


class BaseNestDict:
    """Stores the data in flat object"""

    class __FlattenHelper:
        """Private helper class to handle flattening."""

        @staticmethod
        def flatten(data):
            """
            Flatten the data of dict for easy access
            """

            def _flatten_dict(data, parent_key=""):
                items = {}
                for key, value in data.items():
                    new_key = f"{parent_key}.{key}" if parent_key else key
                    items[new_key] = value
                    if isinstance(value, dict):
                        items.update(_flatten_dict(value, new_key))

                    elif isinstance(value, list):
                        items.update(_flatten_list(value, new_key))

                return items

            def _flatten_list(data, parent_key=""):
                items = {}

                for index, value in enumerate(data):
                    new_key = (
                        f"{parent_key}.[{index}]"
                        if parent_key
                        else f"[{index}]"
                    )
                    items[new_key] = value
                    if isinstance(value, dict):
                        items.update(_flatten_dict(value, new_key))

                    elif isinstance(value, list):
                        items.update(_flatten_list(value, new_key))

                return items

            if isinstance(data, dict):
                return _flatten_dict(data)

            elif isinstance(data, list):
                return _flatten_list(data)

            else:
                raise ValueError(
                    f"Expected data is list or dict got {type(data)}"
                )

    def __init__(self, data=None):
        self.data = data or {}
        self.flatten_dict = self.__FlattenHelper.flatten(self.data)

    def get(self, key_path, default=None):
        return self.flatten_dict.get(key_path, default)

    def __getitem__(self, key_path):
        if key_path not in self.flatten_dict:
            raise KeyError(
                f"{key_path} not found, please check the path again!"
            )

        return self.flatten_dict[key_path]

    def __setitem__(self, key_path, value):
        self.flatten_dict[key_path] = value
        keys = key_path.split(".")

        data = self.flatten_dict
        for index in range(len(keys[:-1])):
            if keys[index] not in data:
                data[keys[index]] = (
                    [{}] if keys[index + 1].startswith("[") else {}
                )
            data = data[keys[index]]

            if isinstance(data, list):
                data = data[0]

        data[keys[-1]] = value

    def delete(self, key_path):
        del self.flatten_dict[key_path]

        keys = key_path.split(".")
        data = self.flatten_dict
        for index in range(len(keys[:-1])):
            data = data[keys[index]]

        del data[keys[-1]]

    def to_dict(self):
        res_dict, res_list = {}, []
        for key, value in self.flatten_dict.items():
            key_list = key.split(".")
            if len(key_list) > 1:
                continue
            parent_key = key_list[0]
            if parent_key.startswith("["):
                res_list.append(value)
            else:
                res_dict[parent_key] = value

        return res_list or res_dict

    def __str__(self) -> str:
        return str(self.to_dict())


class ValidationDict(BaseNestDict):
    def __init__(self, data=None, validation={}):
        super().__init__(data)
        self.validation = validation

        # Validate the data
        if self.validation:
            self._pre_validate()

    def _pre_validate(self):
        for key_path, value in self.validation.items():
            if key_path in self.flatten_dict and not self._validate(
                key_path, self.flatten_dict[key_path]
            ):
                raise ValueError(
                    f"Invalid type for {key_path}: Expected {self.validation.get(key_path).__name__}, got {type(self.flatten_dict[key_path]).__name__}"
                )

    def _validate(self, key_path, value):
        expected_type = self.validation.get(key_path)
        if expected_type and not isinstance(value, expected_type):
            return False
        return True

    def __setitem__(self, key_path, value):
        if not self._validate(key_path, value):
            raise ValueError(
                f"Invalid type for {key_path}: Expected {self.validation.get(key_path).__name__}, got {type(value).__name__}"
            )
        super().__setitem__(key_path, value)


class FrozenDict(BaseNestDict): ...


class NestDict(ValidationDict):
    def __init__(self, data=None, validation={}, frozen=[]):
        ValidationDict.__init__(self, data, validation)
        # FrozenDict.__init__(self, frozen)


# if __name__ == "__main__":
#     data = [
#         {
#             "org_name": "org_1",
#             "location": "New York",
#             "employees": {
#                 "emp_1": {
#                     "name": "test_1",
#                     "age": 43,
#                     "position": "Designer",
#                     "salary": 110420,
#                 },
#                 "emp_2": {
#                     "name": "test_2",
#                     "age": 29,
#                     "position": "Manager",
#                     "salary": 52169,
#                 },
#                 "emp_3": {
#                     "name": "test_3",
#                     "age": 54,
#                     "position": "Developer",
#                     "salary": 71768,
#                 },
#                 "emp_4": {
#                     "name": "test_4",
#                     "age": 46,
#                     "position": "Designer",
#                     "salary": 93011,
#                 },
#                 "emp_5": {
#                     "name": "test_5",
#                     "age": 22,
#                     "position": "Manager",
#                     "salary": 118508,
#                 },
#             },
#         },
#         {
#             "org_name": "org_2",
#             "location": "San Francisco",
#             "employees": {
#                 "emp_1": {
#                     "name": "test_1",
#                     "age": 28,
#                     "position": "Manager",
#                     "salary": 140391,
#                 },
#                 "emp_2": {
#                     "name": "test_2",
#                     "age": 33,
#                     "position": "Manager",
#                     "salary": 81659,
#                 },
#             },
#         },
#     ]

#     n = NestDict(data, validation={"[0].org_name": str})

#     # print(n.flatten_dict)
#     # print(n)
#     # n["[1].a"] = 50
#     # n["[3].[4].b"] = 13
#     # print(n.flatten_dict)
#     # print(n.to_dict())

#     # print(n["[0].employees"])

#     n["[0].org_name"] = "jhgdfj"
#     # print(n["[0].org_name"])

#     n.delete("[0].org_name")
#     # print(n.flatten_dict)
#     print(n)
#     # print(n.flatten_dict)
