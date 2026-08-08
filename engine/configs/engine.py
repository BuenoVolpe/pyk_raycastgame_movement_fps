from engine.configs.base import ConfigsBase
#================================#
class Engine(ConfigsBase):
    def __init__(self, path:str="assets/configs/engine.json"):
        self.asset_marks = None
        #--------------------------------#
        super().__init__(path)
    #================================#
    def set_essential_values(self):
        """set default values for essential game if they are not provided in the JSON"""
        self.render3D = getattr(self,"render3D", True)
        self.max_delta_time_value = getattr(self,"max_delta_time_value", 1)
        self.version = getattr(self,"version", "0.0.0.0")
        self.name = getattr(self,"name", "PyKaizersEngines")
        self.acronym = getattr(self,"acronym", "pyk")
        self.max_fps = getattr(self,"max_fps", 60)
        self.texture_size = getattr(self,"texture_size", 32)
        self.show_fps_in_title = getattr(self,"show_fps_in_title", True)
#================================#
# engine = Engine()
#--------------------------------#
