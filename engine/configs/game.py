from engine.configs.base import ConfigsBase
#================================#
class Game(ConfigsBase):
    def __init__(self, path:str="assets/configs/game.json"):
        #--------------------------------#
        super().__init__(path)
    #================================#
    def set_essential_values(self):
        """set default values for essential game if they are not provided in the JSON"""
        self.window_title = getattr(self,"window_title", "PyKaizersEngine")
        self.name = getattr(self,"name", "PyK_instance")
        self.acronym = getattr(self,"acronym", "pykinst")
        #--------------------------------#
        self.version = getattr(self,"version", "0.0.0.0")
        #--------------------------------#
        # self.window_size = getattr(self,"window_size", [640,360])
        # self.window_width, self.window_height = self.window_size
        # self.window_center = self.window_width//2, self.window_height//2
        #--------------------------------#
        self.base_window_size = getattr(self,"base_window_size", [320,180])
        self.base_window_width, self.base_window_height = self.base_window_size
        self.base_window_center = self.base_window_width//2, self.base_window_height//2
#================================#
# game = Game()
#--------------------------------#