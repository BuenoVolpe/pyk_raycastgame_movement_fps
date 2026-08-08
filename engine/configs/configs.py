from engine.configs.base import ConfigsBase
from engine.configs.paths import Paths
from engine.configs.game import Game#, game
from engine.configs.engine import Engine#, engine
from engine.configs.inputs import inputs
# from engine.configs.debug import Debug
#================================#
from engine.utils.json import json_reader, scan_folder
#================================#
class ConfigManager:
    #--------------------------------#
    def __init__(self):
        self.paths = Paths()
        self.game = Game(self.paths.game.configs)
        self.inputs = inputs
        self.engine = Engine(self.paths.engine.configs)
        # self.debug = Debug(self.paths.debug.configs)
        #--------------------------------#
        self.fonts:list = None
        #--------------------------------#
        self._load_others_configs(self.paths.configs)

    #================================#
    def _load_others_configs(self, path:str):
        #--------------------------------#
        jsons = scan_folder(path, ".json")
        #--------------------------------#
        for i, (j_path, name) in enumerate(jsons):
            #--------------------------------#
            if hasattr(self, name.lower()):
                continue
            #--------------------------------#
            data = json_reader(j_path, {})
            #--------------------------------#
            setattr(self, name.lower(), ConfigsBase(j_path))
    #================================#
    def set(self, config:str, key:str, value=None):
        #--------------------------------#
        config = getattr(self, config.lower())
        #--------------------------------#
        if config:
            config.set(key, value)
    #================================#
    def save(self, config:str):
        #--------------------------------#
        config = getattr(self, config.lower())
        #--------------------------------#
        if config:
            config.save()
    #================================#
    def reload(self, config:str):
        #--------------------------------#
        config = getattr(self, config.lower())
        #--------------------------------#
        if config:
            config.reload()
    #================================#
    def get_data(self, config:str) -> dict:
        config = getattr(self, config.lower())
        #--------------------------------#
        if not config:
            return {}
        #--------------------------------#
        return config._data
    #================================#
    def get(self, config:str, key:str, default_value:any=None) -> any:
        #--------------------------------#
        config = getattr(self, config.lower())
        #--------------------------------#
        if not config:
            return default_value
        #--------------------------------#
        return config.get(key, default_value)
#================================#
configs = ConfigManager()#
