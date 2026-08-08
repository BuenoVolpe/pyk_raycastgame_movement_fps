import pygame as pg
import time
#=====================================#
from engine.configs.configs import configs
#=====================================#
from engine.console.utils import parse_args, parse_value, split_command
#=====================================#
from engine.handlers.fonts import fonts
from engine.utils.wrap_text import wrap_text
from engine.utils.debug_log import log_error, log_success
#=====================================#
from engine.signal_bus import signal_bus
from game.enums.signals import signals
from game.enums.signals_prioritys import signals_prioritys
#=====================================#
from dataclasses import dataclass
#=====================================#
class ConsoleLog:
    def __init__(self, width):
        self.width = width
        self.font = fonts.get(configs.console.font).get_size(configs.console.font_size)
        #-------------------------------------#        
        self.lines = []
        self.max_lines = configs.console.max_log_lines

    #=====================================#
    def _add(self, text, color="white", styles=None):

        wrapped_lines = wrap_text(
            str(text),
            self.font,
            self.width
        )

        for line in wrapped_lines:
            self.lines.append(
                LogLine(line, color, styles or [])
            )

        while len(self.lines) > self.max_lines:
            self.lines.pop(0)
    #=====================================#
    def log(self, text, color="white", styles=None):
        self._add(str(text), color, styles)
    #=====================================#
    def log_error(self, text):
        self._add(f"!> {text}", "red", ["bright"])
    #=====================================#
    def log_success(self, text):
        self._add(f">>[ {text} ]<<", "yellow", ["bright"])
    #=====================================#
    def log_command(self, text):
        self._add(f"> {text}", "cyan", ["bright"])
    #=====================================#
    def log_list(self, list:list, color:str="white", styles:list=None, list_name:str=None, list_color:str=None, list_styles:list=None):
        #-------------------------------------#        
        self.log(f"#========= {list_name} =========#", list_color, list_styles)
        #-------------------------------------#        
        for item in list:
            self._add(str(item), color, styles)
    #=====================================#
    def log_dict(self, dict:dict,
                value_color:str=None,
                styles:list[str|None, str|None]=[],
                dict_name=None, name_color:str=None, name_styles:list[str|None, str|None]=None):
        #-------------------------------------#        
        self.log(f"#========= {dict_name} =========#", name_color, name_styles)
        #-------------------------------------#        
        for k, v in dict.items():
            self._add(f"{k}: {v}", value_color, styles)
#=====================================#
@dataclass
class LogLine:
    #-------------------------------------#
    text: str
    color: str = "white"
    styles: list = None
    timestamp: float = time.time()
    #-------------------------------------#
    def __post_init__(self):
        #-------------------------------------#
        if self.styles is None:
            self.styles = []
