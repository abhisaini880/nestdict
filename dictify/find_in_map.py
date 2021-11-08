""" 
# Implementation for FIND_IN_MAP Function 

    * Basic functionality for FIND_IN_MAP function is to search nested dicts
    or nested key-value pair.  

    * It accepts muliple args in which first arg is the dict object and rest
    are the keys in dict object.

    * find_in_map(dict_obj, parent_key, child_key, child_key_2) --> It returns
    the value for child_key_2 value

    * In case the result is not found then return NULL

    * It can be used to find the value of nested key or search for nested key if present.
"""

__all__ = ["find_in_map"]


def find_in_map(obj, *args):
    """
    It accepts the dict object and nested keys and return the value
    of last key if present in nested key is present in object.

    Args:
        obj (dict): dict object

    Returns: Value of last nested key
    """
    if not isinstance(obj, dict):
        # raise InvalidRequestException
        print("Exception raised !")
        return

    nested_keys = list(args)

    for key in nested_keys:
        obj = _iterate_over_nested_obj(obj, key)
        if obj is None:
            return

    return obj


def _iterate_over_nested_obj(obj, key):
    """It iterates over the nested dict object.
    It iterates over two types of data
    * list
    * dict

    for the rest data type it returns the value

    Args:
        obj (any type): object to process
        key (str, int): key to find in object
    """

    if isinstance(obj, dict):
        if obj.get(key):
            return obj[key]
    elif isinstance(obj, list):
        for item in obj:
            value = _iterate_over_nested_obj(item, key)
            if value:
                return value
        return None
    else:
        return None
