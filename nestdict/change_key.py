"""# implementation of change_value function

    * It changes the name of perticular key and returns back the dictionary.
    * It also works with nested dictionary

    USECASE 1:

        dic = {
            "cars_owned":{
            "sedan":1,
            "suv":3
            }
        }

        print("\noriginal dictionary :",dic)
        
        change_key = nestdict.change_key(dic,"sedan","tesla")

        print("\nchange_key function :",change_key)


        OUTPUT:

        original dictionary : {'cars_owned': {'sedan': 1, 'suv': 3}}

        change_key function : {'cars_owned': {'tesla': 1, 'suv': 3}}

    USECASE 2:

        dic = {
            "cars_owned":{
            "sedan":1,
            "suv":3
            }
        }

        print("\noriginal dictionary :",dic)
        
        nestdict.change_key(dic,"sedan","tesla")

        print("\nchange_value function :",dic)


        OUTPUT:

        original dictionary : {'cars_owned': {'sedan': 1, 'suv': 3}}

        change_key function : {'cars_owned': {'tesla': 10, 'suv': 3}}
        
"""

def change_key(obj,from_old_key,to_new_key):

    """
       This function accept three params
       and iterats over the obj(dict) and
       replaces the old key.

       Arg:

           obj (dict) : dictionary object
           from_old_key : pass the key the you wanted to change.
           to_new_key : pass the new key to replace insisted of old key.

        for more understanding see README.md
    """

    for key,value in obj.items():
        if key == from_old_key:
            obj[to_new_key] = obj[from_old_key]
            obj.pop(from_old_key)
            break
        elif isinstance(value,dict):
            change_key(value,from_old_key,to_new_key)
            
    return obj
