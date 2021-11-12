"""# implementation of change_value function

    * It changes the value of a perticular key and returns back the dictionary.
    * It also works with nested dictionary.

    USECASE 1:

        dic = {
            "cars_owned":{
            "sedan":1,
            "suv":3
            }
        }

        print("\noriginal dictionary :",dic)
        
        change_value = nestdict.change_value(dic,"sedan",10)

        print("\nchange_value function :",change_value)


        OUTPUT:

        original dictionary : {'cars_owned': {'sedan': 1, 'suv': 3}}

        change_value function : {'cars_owned': {'sedan': 10, 'suv': 3}}

    USECASE 2:

        dic = {
            "cars_owned":{
            "sedan":1,
            "suv":3
            }
        }

        print("\noriginal dictionary :",dic)
        
        nestdict.change_value(dic,"sedan",10)

        print("\nchange_value function :",dic)


        OUTPUT:

        original dictionary : {'cars_owned': {'sedan': 1, 'suv': 3}}

        change_value function : {'cars_owned': {'sedan': 10, 'suv': 3}}
        
"""

def change_value(obj,key,value):

    """
       This function accept three params
       and iterats over the obj(dict) and replace value
       of the key

       Arg:

           obj (dict) : dictionary object
           key : pass the key.
           value = value to be replaced insitited of previous value

        for more understanding see README.md
    """
    for k,v in obj.items():
            if key == k:
                obj[key] = value
                break
            elif isinstance(v,dict):
                change_value(v,key,value)

    return obj

