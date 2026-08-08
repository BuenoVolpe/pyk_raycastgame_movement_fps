#--------------------------------#
from pathlib import Path
#--------------------------------#
from engine.utils.log import log, log_success, log_error
from engine.utils.json import json_reader, json_writer
#--------------------------------#
class ConfigsBase:
    #--------------------------------#
    def __init__(self, path:str|dict="assets/config/settings.json"):
        #--------------------------------#
        if isinstance(path, dict):
            self.set_dynamically_settings(path)
            self._path = None
            return
        #--------------------------------#
        self._path = Path(path)
        self._data = json_reader(path)
        #--------------------------------#
        # Dynamically set any additional settings from the JSON file
        #--------------------------------#
        self.set_dynamically_settings(self._data)
        #--------------------------------#
        self.set_essential_values()
    #--------------------------------#
    def set_essential_values(self):
        """set default values for essential configs if they are not provided in the JSON"""
        ...
    #--------------------------------#
    def get_path(self, path:str):
        node = self

        for key in path.split("."):
            if not hasattr(node, key):
                return None

            node = getattr(node, key)

        return node
    #--------------------------------#
    def create_subclass(self, data:dict, name:str):
        #--------------------------------#
        subclass = ConfigsBase(data)
        setattr(self, name, subclass)
    #--------------------------------#
    def set_dynamically_settings(self, data:dict):
        #--------------------------------#
        for key, value in data.items():
            #--------------------------------#
            if isinstance(value, dict):
                #--------------------------------#
                if value.get("subclass", False):
                    self.create_subclass(value, key)
                    continue
            #--------------------------------#
            setattr(self, key, value)
        #--------------------------------#
        if not hasattr(self, "_data"):
            self._data = data

    #----get method---#
    def get(self, key:str, default=None):
        if hasattr(self, key):
            return getattr(self, key)
        return default
    #----set method---#
    def set(self, key:str, value=None):
        #--------------------------------#
        if callable(getattr(self, key, None)):
            raise ValueError(f"Cannot overwrite method '{key}'")
        #--------------------------------#
        setattr(self, key, value)
        #--------------------------------#
        self._data[key] = value
        #--------------------------------#
        self.save()
    #----save method---#
    def save(self):
        #--------------------------------#
        json_writer(self._path, self._data)
        log_success(f"{self.__class__.__name__} saved: {self._path}")

    #----reload method---#
    def reload(self):
        #--------------------------------#
        self._data = json_reader(self._path)
        self.set_essential_values()
        #--------------------------------#
        for key, value in self._data.items():
            setattr(self, key, value)
        #--------------------------------#
        log(f"{self.__class__.__name__} reloaded")
#--------------------------------#

