# Nestdict
## _Makes Nested Dictionaries Easy To Use_

[![Python](https://www.python.org/static/community_logos/python-powered-w-140x56.png)](https://docs.python.org/3/)

Nestdict is used to simplify various operations on nested and plain dictionaries.
It offers various functions to simplify your work.

- Pass the dictionary object in the function of your need.
- Get the result you want.

## Functions

- *find_in_map(dict_obj, key1, key2, key3, ...)*  `finds the value for nested keys if exist.`
   ```py
   obj = {
       "cars_owned": {
         "sedan": 1,
         "suv": 3,
         "hatchback": 2
       },
   }
   
   suv_cars_count = find_in_map(obj, "cars_owned", "suv")
   
   print(suv_cars_count) >> 3
   ```
- *all_keys(dict_obj)* `returns all the keys present in the object`
    ```py
   obj = {
       "cars_owned": {
         "sedan": 1,
         "suv": 3,
         "hatchback": 2
       },
   }
   
   car_types = all_keys(obj["cars_owned"])
   all_keys_in_obj = all_keys(obj)
   
   print(car_types) >> ["sedan", "suv", "hachback"]
   print(all_keys_in_obj) >> ["cars_owned", "sedan", "suv", "hachback"]
   ```
- *check_keys(dict_obj, [key1, key2, ...])* `check if all the keys exist in object`
    ```py
    obj = {
       "cars_owned": {
         "sedan": 1,
         "suv": 3,
         "hatchback": 2
       },
   }
   
   is_sedan_and_suv_exist = check_keys(obj, ["sedan", "suv"])
   
   print(is_sedan_and_suv_exist) >> True
   ```

## Installation

Nestdict requires Python3.6 +

Install using pip

```sh
pip install nestdict
```

Import functions from nestdict

```py
from nestdict import find_in_map,check_keys
```

## Development

Want to contribute? Great!
1. Fork the repository.
2. Clone the Project and create a seprate branch with function name(`/feature/<featureName>`) or bug name(`/bugfix/<brief>`).
3. Make sure to clearly describe the functionality and use case.
4. Make a pull request.