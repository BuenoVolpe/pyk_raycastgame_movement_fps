#=====================================#
import pygame as pg
import os
#-------------------------------------#
from engine.configs.configs import configs
from engine.utils.scaler import scaler
#-------------------------------------#
from engine.signal_bus import signal_bus
from game.enums.signals import signals
#=====================================#
class Display:
    #=====================================#
    def __init__(self):
        self._load_screen()
    #=====================================#
    def _load_screen(self):
        window_title:str = configs.game.window_title
        #=====================================#
        RES = self.get_screen_resolution()
        MIN_RES:list[int, int] = configs.game.base_window_size
        #--------------------------------#
        self.screen = pg.display.set_mode(RES)
        self.main_surface = pg.Surface(MIN_RES, pg.SRCALPHA)
        #--------------------------------#
        pg.display.set_caption(window_title)
        pg.scrap.init()
    #=====================================#
    def get_screen_resolution(self) -> list[int, int]:
        #--------------------------------#
        RES:list[int, int] = configs.settings.window_size
        #--------------------------------#
        use_full_screen = configs.settings.full_screen
        #--------------------------------#
        if use_full_screen:
            #------------------------------#
            os.environ["SDL_VIDEO_CENTERED"] = "1"
            info = pg.display.Info()
            #------------------------------#
            WIDTH:int = info.current_w
            HEIGHT:int = info.current_h
            RES:list[int, int] = [WIDTH, HEIGHT]
            configs.settings.window_width, configs.settings.window_height = configs.settings.window_size = RES
            configs.settings.window_center = RES[0]//2, RES[1]//2
            #------------------------------#
            signal_bus.emit(signals.DISPLAY_BUILDED_SCREEN)
        #------------------------------#
        return RES
    