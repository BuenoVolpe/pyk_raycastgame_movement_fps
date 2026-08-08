import pygame as pg
from sys import exit, executable, argv
import os
#--------------------------------#
from pathlib import Path
#--------------------------------#
from engine.utils.log import log, log_success, log_error
from engine.utils.json import json_reader, json_writer
#--------------------------------#
from engine.configs.base import ConfigsBase
from engine.configs.paths import paths
#================================#
class Inputs(ConfigsBase):
    #================================#
    def __init__(self, path:str = "assets/config/inputs.json"):
        self.inputs:dict = {}
        #--------------------------------#
        super().__init__(path)
    #================================#
    def set_essential_values(self):
        self._load_input_keys()
    #================================#
    def _load_input_keys(self):
        #--------------------------------#
        raw_keys = self._data
        #--------------------------------#
        mouse_map = {
            "LMB": pg.BUTTON_LEFT,
            "RMB": pg.BUTTON_RIGHT,
            "MMB": pg.BUTTON_MIDDLE,
        }
        #--------------------------------#
        fundamental_defaults = {
            "up": "w",
            "down": "s",
            "left": "a",
            "right": "d",
            "menu": "escape",
            "quit": "Lalt",
            **mouse_map
        }
        #--------------------------------#
        # merge defaults + json overrides
        merged = {**fundamental_defaults, **raw_keys}
        #--------------------------------#
        for name, value in merged.items():
            #--------------------------------#
            # mouse
            if value in mouse_map:
                self.inputs[name] = mouse_map[value]
                continue
            #--------------------------------#
            # keyboard
            try:
                keycode = pg.key.key_code(str(value).lower())
                self.inputs[name] = keycode
            #--------------------------------#
            except ValueError:
                #--------------------------------#
                if str(value).lower() in ["lalt", "lctrl", "lshift", "ralt", "rctrl", "rshift", "minus", "lmb", "rmb", "mmb", "enter", "escape"]:
                    #--------------------------------#
                    special_keys = {
                        "lalt": pg.K_LALT,
                        "lctrl": pg.K_LCTRL,
                        "lshift": pg.K_LSHIFT,
                        "ralt": pg.K_RALT,
                        "rctrl": pg.K_RCTRL,
                        "rshift": pg.K_RSHIFT,
                        "minus": pg.K_MINUS,
                        "lmb": pg.BUTTON_LEFT,
                        "rmb": pg.BUTTON_RIGHT,
                        "mmb": pg.BUTTON_MIDDLE,
                        "enter": pg.K_RETURN,
                        "escape": pg.K_ESCAPE
                    }
                    #--------------------------------#
                    self.inputs[name] = special_keys[str(value).lower()]
                #--------------------------------#
                else:
                    #--------------------------------#
                    log_error(f"[KEY ERROR] Invalid key: {value}")
    #================================#
    def pyinput(self, prompt:str = "input: ") -> str|None|float:
        return input(prompt)
    #================================#
    def input(self, key:str, default_key_value:int=None) -> bool:
        #--------------------------------#
        keycode = self.inputs.get(key, default_key_value)
        #--------------------------------#
        if keycode is None:
            return False
        #--------------------------------#
        keys = pg.key.get_pressed()
        #--------------------------------#
        return keys[keycode]
    #================================#
    def input_by_event(self, event, key:str, default_key_value:int=None, form:str="down") -> bool:
        #--------------------------------#
        if event.type in [pg.KEYDOWN, pg.KEYUP, 1]:
            #--------------------------------#
            if form == "down" and event.type == pg.KEYDOWN:
                return event.key == self.event_input(key, default_key_value)
            #--------------------------------#
            elif form == "up" and event.type == pg.KEYUP:
                return event.key == self.event_input(key, default_key_value)
        #--------------------------------#
        elif event.type in [pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP, 0]:
            #--------------------------------#
            if form == "down" and event.type == pg.MOUSEBUTTONDOWN:
                return event.button == self.event_input(key, default_key_value)
            #--------------------------------#
            elif form == "up" and event.type == pg.MOUSEBUTTONUP:
                return event.button == self.event_input(key, default_key_value)
    #================================#
    def event_input(self, key:str, default_key_value:int=None):
        #--------------------------------#
        if self.inputs.get(key, default_key_value):
            #--------------------------------#
            return self.inputs.get(key, default_key_value)
        #--------------------------------#
        return default_key_value
#================================#
inputs = Inputs(paths.inputs)
#================================#
# value = inputs.pyinput("hello: ") #input("hello: "))

# if inputs.input(key="up", pg.K_up):
#     x -= 5

# for event in pg.event.get():
#     ##can be keydown, keyup, mousebuttondown, mousebuttonup
#     if inputs.input_by_event(event, key="up", form="down"):
#         ... do something when the "up" key is pressed down

# for event in pg.event.get():
    # if event.type == pg.KEYDOWN and event.key == inputs.event_input("quit", pg.K_LALT):
    #     ...