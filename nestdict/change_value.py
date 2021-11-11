"""# implementation of change_value function

    * it changes the value of a particular key and returns the dictionary back.
    * it also works with nested dictionary.
"""
    
def change_value(obj,*args,value):
    
    """This function accept three params
       and iterats over the obj(dict) and replace value
       of the key.
       
       Arg:
         obj (dict) = dictionary object.
         *args (list) = must pass the keys in a list.
         value = value to replace insitited of old value
         
       Note: *args must be in correct order.
       Use Case:
             dic = {
                   "cars_owned :{
                   "sedan":1,
                   "suv":3
                   },
                }
                
             print("original :", dic)
             print(nestdict.change_value(dic,["cars_owned","suv"],value = 100))
             
             #the elements inside the list must follow the correct order.
             
       output:
       
       original : {"cars_owned":{"sedan":1,"suv":3},}
       
       {"cars_owned":{"sedan":1,"suv":100},}
       
       
         
      for more understanding read README.md
      """

    changed_obj = obj
    
    keys = list(*args)
    
    if len(keys)>1:
        for element in keys:
            obj = obj[element]
            try:
                if obj.get(keys[-1]):
                        obj[keys[-1]] = value
                        break
            except:
                raise ValueError('{} is not a valid argument.'.format(keys))
            
    elif len(keys) == 1:
        changed_obj[keys[0]] = value
            
    return changed_obj
