from engine.configs.configs import configs
#------------------------------#
from game.enums.assets_marks import assetsmarks
from engine.utils.debug_log import debug_log
#------------------------------#
import pygame as pg
#================================#
from engine.utils.dict_to_class import dict_to_class
from engine.utils.wrap_text import wrap_text
from engine.utils.log import log_error
from engine.utils.json import scan_folder
from engine.utils.scaler import scaler
#================================#
pg.init()
#================================#
class Font:
    def __init__(self, path:str):
        self.path = path
        #------------------------------#
        self.fonts = {}
        #------------------------------#
        for i in range(1, 101):  # Example: Create fonts for sizes 1 to 100
            self.fonts[i] = pg.font.Font(path, scaler.constant(i))
            setattr(self, f"size_{i}", self.fonts[i])  # Set attributes like size_10, size_20, etc.
        #------------------------------#
        self.size_10 = pg.font.Font(path, scaler.constant(10))
        self.size_20 = pg.font.Font(path, scaler.constant(20))
        self.size_30 = pg.font.Font(path, scaler.constant(30))

    #================================#
    def get_size(self, size):
        #------------------------------#
        font = getattr(self, f"size_{size}", None)
        #------------------------------#
        if not font:
            log_error(f"cannot find size {size}, returning size 10")
            return self.size_10
        #------------------------------#
        return font

    #================================#
    def render(
        self,
        surface: pg.Surface,
        pos: tuple[int, int],
        text: str,
        size: int = 10,
        color=(255,255,255),
        bgcolor=None,
        aligment="topleft",
        wrap_width: int | None = None,
        line_spacing: int = 2
    ):
        font = self.fonts.get(size, self.size_10)

        if wrap_width is None:
            text_surface = font.render(text, True, color, bgcolor)

            text_rect = text_surface.get_rect()
            setattr(text_rect, aligment, pos)

            surface.blit(text_surface, text_rect)
            return

        lines = wrap_text(text, font, wrap_width)

        line_height = font.get_height() + line_spacing

        x, y = pos

        for i, line in enumerate(lines):
            text_surface = font.render(line, True, color, bgcolor)
            text_rect = text_surface.get_rect()

            setattr(text_rect, aligment, (x, y + i * line_height))

            surface.blit(text_surface, text_rect)

        return len(lines) * line_height

#------------------------------#    
fonts = dict_to_class({})
bases = [
    configs.paths.engine.fonts,
    configs.paths.game.fonts
]
#------------------------------#
def get_font(font_name):
    if font := getattr(fonts, font_name):
        if isinstance(font, pg.font.Font):
            return font
    else:
        return fonts.engine_default
#------------------------------#
fonts.engine_default = Font(configs.paths.default_font)
fonts.get_font = get_font
#------------------------------#
for base in bases:
    for font_path, font_name in scan_folder(base, extension=f".{configs.engine.extensions.font}"):
        #------------------------------#    
        font = Font(font_path)
        debug_log(f"{assetsmarks.engine.debug}::fonts.being_created", f"name: {font_name}, path: {font_path}")
        #------------------------------#    
        setattr(fonts, font_name, font)
#================================#

