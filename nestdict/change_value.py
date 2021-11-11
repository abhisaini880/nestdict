
def change_value(obj,*args,value):

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
