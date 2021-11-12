"""# implementation of change_value function

    * It changes the value of a perticular key and returns back the dictionary back.
    * It also works with nested dictionary.

    USECASE 1:

        dic = {
            "cars_owned":{
            "sedan":1,
            "suv":3
            }
        }

        print("\noriginal dictionary :",dic)

        keys = ["cars_owned","sedan"]
        
        change_value = nestdict.change_value(dic,keys,value = 10)

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

        keys = ["cars_owned","sedan"]
        
        nestdict.change_value(dic,keys,value = 10)

        print("\nchange_value function :",dic)


        OUTPUT:

        original dictionary : {'cars_owned': {'sedan': 1, 'suv': 3}}

        change_value function : {'cars_owned': {'sedan': 10, 'suv': 3}}
        
"""

def change_value(obj,*args,value):

    """
       This function accept three params
       and iterats over the obj(dict) and replace value
       of the key

       Arg:

           obj (dict) : dictionary object
           *args (list) : must pass the keys in a list.
           value = value to be replaced insitited of previous value

        Note: *args must follow the correct key order.

        for more understanding see README.md
    """
            

    changed_obj = obj
    
    keys = list(*args)
    
    if len(keys)>1:
        
        for key in keys:
            
            if obj.get(key):
                obj = obj[key]
                if obj.get(keys[-1]):
                        obj[keys[-1]] = value
                        break
                else:
                    return None
            else:
                return None
            

           
    elif len(keys) == 1:
        
        if obj.get(keys[0]):
            changed_obj[keys[0]] = value
        else:
            return None

    return changed_obj
