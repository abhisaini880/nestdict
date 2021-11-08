"""
# Implementation of all_keys function.

    * It will return all the keys present in the object.

    * It will also return the nested keys at all levels.

"""

__all__ = ["all_keys"]


def _recursive_items(dictionary):
    """This function will accept the dictionary
        and iterate over it and yield all the keys

    Args:
        dictionary (dict): dictionary to iterate

    Yields:
        string: key in dictionary object.
    """
    for key, value in dictionary.items():
        yield key
        if isinstance(value, dict):
            yield from _recursive_items(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    yield from _recursive_items(item)
        else:
            yield key


def all_keys(obj):
    """This function will accept one param
        and return all keys
        * It will return all the keys in the object

    Args:
        obj (dict): dictionary object

    Returns:
        set: set of all the keys
    """
    key_from_obj = set()
    for key in _recursive_items(dictionary=obj):
        key_from_obj.add(key)
    return key_from_obj
