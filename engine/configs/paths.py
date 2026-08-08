from engine.configs.base import ConfigsBase
#================================#
class Paths(ConfigsBase):
    def __init__(self, path:str="assets/configs/paths.json"):
        #--------------------------------#
        super().__init__(path)
    #================================#
    def set_essential_values(self):
        """set default values for essential paths if they are not provided in the JSON"""
        self.configs = getattr(self, "configs", "assets/configs/")
        #--------------------------------#
        self.inputs = getattr(self, "inputs", "assets/configs/inputs.json")
        self.paths = getattr(self, "paths", "assets/configs/paths.json")
        #--------------------------------#
#================================#
paths = Paths()
#--------------------------------#