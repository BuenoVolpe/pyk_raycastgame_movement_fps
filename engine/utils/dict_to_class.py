def dict_to_class(data:dict):
    #--------------------------------#
    obj = GenericClass()
    #--------------------------------#
    if not isinstance(data, dict):
        return data
    #--------------------------------#
    for key, value in data.items():
        #--------------------------------#
        if isinstance(value, dict):
            #--------------------------------#
            if value.get("subclass", False):
                value = dict_to_class(value)
                continue
        #--------------------------------#
        setattr(obj, key, value)
    #=====================================#
    obj._data = data
    #--------------------------------#
    return obj
#=====================================#
class GenericClass:
    ...
    #--------------------------------#
    def get(self, key:str, default_value:any=None) -> any:
        return getattr(self, key, default_value)


