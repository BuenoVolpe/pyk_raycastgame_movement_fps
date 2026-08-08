import pygame as pg
from engine.configs.configs import configs
#--------------------------------#
from engine.signal_bus import signal_bus
from game.enums.signals import signals
from game.enums.signals_prioritys import sig_prio
#------------------------------#
class Scaler:
    """
    Handles resolution scaling for the game.

    This class converts values and surfaces from base resolution
    into the current window resolution.
    """
    #------------------------------#
    def __init__(self):
        #------------------------------#
        self.update()
        signal_bus.subscribe(signals.DISPLAY_BUILDED_SCREEN, self.update, sig_prio.UPDATE_GLOBAL_OBJ)
    #------------------------------#
    def update(self):
        game = configs.game
        settings = configs.settings
        #------------------------------#
        # Ratio between current window size and base window size
        self.W_RATIO = settings.window_size[0] / game.base_window_width
        self.H_RATIO = settings.window_size[1] / game.base_window_height
    #------------------------------#
    def constant(self, value: float) -> int:
        return int(value * configs.game.get("constant_scale", 1) * min(self.W_RATIO, self.H_RATIO))
    #------------------------------#
    def scale(self, value: float) -> int:
        return int(value * min(self.W_RATIO, self.H_RATIO))
    #------------------------------#
    def scale_list(self, list:list, use_scale_constant=False) -> pg.Surface:
        if use_scale_constant:
            result = [self.constant(i) for i in list]
        else:
            result = [self.scale(i) for i in list]
        return result
    #------------------------------#
    def surface(self, image: pg.Surface, resolution="auto", use_scale_constant=False) -> pg.Surface:
        #------------------------------#
        if resolution is None:
            return image
        #------------------------------#
        # Auto scaling based on original surface size
        if resolution == "auto":
            #------------------------------#
            if use_scale_constant:
                w = self.constant(image.get_width())
                h = self.constant(image.get_height())
            else:
                w = self.scale(image.get_width())
                h = self.scale(image.get_height())
            #------------------------------#
            return pg.transform.scale(image, (w, h))
        #------------------------------#
        # Manual scaling based on custom resolution
        if use_scale_constant:
            w = self.constant(resolution[0])
            h = self.constant(resolution[1])
        else:
            w = self.scale(resolution[0])
            h = self.scale(resolution[1])
        #------------------------------#
        return pg.transform.scale(image, (w, h))
    #------------------------------#
    def coordenates(self, x,y) -> list[int, int]:
        #------------------------------#
        scalled_x = int(self.W_RATIO * x)
        scalled_y = int(self.H_RATIO * y)
        #------------------------------#
        return (scalled_x, scalled_y)
    #------------------------------#
    def descale_constant(self, value: float) -> int:
        #------------------------------#
        return int(value / (configs.game.scale_constant * min(self.W_RATIO, self.H_RATIO)))
    #------------------------------#
    def descale_coordinates(self, x, y) -> tuple[int, int]:
        #------------------------------#
        base_x = int(x / self.W_RATIO)
        base_y = int(y / self.H_RATIO)
        #------------------------------#
        return base_x, base_y
#------------------------------#
scaler = Scaler()
#------------------------------#
