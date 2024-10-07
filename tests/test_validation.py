import unittest
from nestdict import NestDict


class TestValidationDict(unittest.TestCase):

    def setUp(self):
        self.sample_data = {
            "user": {"name": "Alice", "age": 30},
            "preferences": {"language": ["English", "French"]},
        }

    def test_valid_data_with_validation(self):
        validation = {"user.name": str, "user.age": int}
        nest_dict = NestDict(data=self.sample_data, validation=validation)
        self.assertEqual(nest_dict.get("user.name"), "Alice")

    def test_invalid_data_type(self):
        validation = {"user.name": str, "user.age": str}
        with self.assertRaises(ValueError):
            NestDict(data=self.sample_data, validation=validation)

    def test_set_with_invalid_type(self):
        validation = {"user.age": int}
        nest_dict = NestDict(data=self.sample_data, validation=validation)
        with self.assertRaises(ValueError):
            nest_dict["user.age"] = "thirty"

    def test_set_with_valid_type(self):
        validation = {"user.age": int}
        nest_dict = NestDict(data=self.sample_data, validation=validation)
        nest_dict["user.age"] = 35
        self.assertEqual(nest_dict.get("user.age"), 35)
