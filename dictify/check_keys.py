""" 
# Implementation of check_keys function

    * This Function will check for the keys in dictionary
        and return True if all keys are found. 
    
    * It's a atomic function means it will only return True
        if all keys are found in the object else False.
    
    * It can also check for nested keys.

"""

__all__ = ["check_keys"]


def check_keys(obj, required_key_list):
    """This function will accept two params
        and return a boolean value.
        * It will check if all keys are present in the object

    Args:
        required_key_list (list): list of required keys
        obj (dict): dictionary object to be checked.

    Returns:
        bool: True if all keys are present else False
    """
    key_from_obj = set()
    for key in _recursive_items(dictionary=obj):
        key_from_obj.add(key)
    for key in required_key_list:
        if key not in key_from_obj:
            return False
    return True


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
