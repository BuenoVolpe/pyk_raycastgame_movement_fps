from engine.configs.configs import configs

class Camera:
    #=====================================#
    def __init__(self, target=None):
        #-------------------------------------#
        self.x = 0
        self.y = 0
        #-------------------------------------#
        self.target = target
        #-------------------------------------#
        self.offset_x = 0
        self.offset_y = 0
    #=====================================#
    def follow(self, position, surface):
        #-------------------------------------
        self.x += ((position[0] - self.x) * configs.settings.camera_smoothing - surface.get_width()//2)
        self.y += ((position[1] - self.y) * configs.settings.camera_smoothing - surface.get_height()//2)
    #=====================================#
    def world_to_screen(self, x, y):
        #-------------------------------------#
        return (
            x - self.x + self.offset_x,
            y - self.y + self.offset_y
        )
    

