# import unittest
# from your_module import FrozenDict


# class TestFrozenDict(unittest.TestCase):

#     def setUp(self):
#         self.sample_data = {"user": {"name": "Alice", "age": 30}}

#     def test_freeze_keys(self):
#         frozen_keys = ["user.age"]
#         nest_dict = FrozenDict(data=self.sample_data, frozen_keys=frozen_keys)
#         with self.assertRaises(TypeError):
#             nest_dict["user.age"] = 31

#     def test_freeze_after_set(self):
#         nest_dict = FrozenDict(data=self.sample_data)
#         nest_dict["user.name"] = "Bob"
#         nest_dict.freeze_keys(["user.name"])
#         with self.assertRaises(TypeError):
#             nest_dict["user.name"] = "Charlie"

#     def test_non_frozen_keys_still_modifiable(self):
#         frozen_keys = ["user.age"]
#         nest_dict = FrozenDict(data=self.sample_data, frozen_keys=frozen_keys)
#         nest_dict["user.name"] = "Bob"
#         self.assertEqual(nest_dict.get("user.name"), "Bob")
