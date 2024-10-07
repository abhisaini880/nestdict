import unittest
from nestdict import NestDict


class TestNestDict(unittest.TestCase):

    def setUp(self):
        self.sample_data = {
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
        self.nest_dict = NestDict(data=self.sample_data)

    def test_get_existing_key(self):
        self.assertEqual(self.nest_dict.get("user.name"), "Alice")
        self.assertEqual(
            self.nest_dict.get("user.address.city"), "Wonderland"
        )

    def test_get_non_existing_key(self):
        self.assertIsNone(self.nest_dict.get("user.phone"))

    def test_set_new_key(self):
        self.nest_dict["user.phone"] = "123-456"
        self.assertEqual(self.nest_dict.get("user.phone"), "123-456")

    def test_delete_key(self):
        self.nest_dict.delete("user.address.city")
        self.assertIsNone(self.nest_dict.get("user.address.city"))
        dict_data = self.nest_dict.to_dict()
        self.assertIsNone(
            dict_data.get("user", {}).get("address", {}).get("city")
        )
