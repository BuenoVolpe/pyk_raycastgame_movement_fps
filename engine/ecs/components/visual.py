import pygame as pg
import numpy as np
import math
#================================#
from engine.ecs.component_storage import register_engine_component
#--------------------------------#
from engine.utils.globalclasses import globalclasses
from engine.utils.dict_to_class import dict_to_class
#================================#
@register_engine_component
class SimpleAnimation:
    #--------------------------------#
    def __init__(self, textures:list, fps:float, convert_into_texture=False):
        #--------------------------------#
        if convert_into_texture:
            self.textures = [globalclasses.TextureHandler.get(tex) for tex in textures]
        else:
            self.textures = textures
        self.fps = fps
        #--------------------------------#
        self.current_frame = 0
        self.timer = 0
        #--------------------------------#
        self.frame_time = 1 / fps
#================================#
@register_engine_component
class StateAnimation:
    #--------------------------------#
    def __init__(self, **states:dict):
        #--------------------------------#
        self.states = {}
        #--------------------------------#
        for key, animation_data in states.items():
            #--------------------------------#
            self.states[key] = SimpleAnimation(**animation_data)
        #--------------------------------#
        self.current_frame = 0
        self.timer = 0
        #--------------------------------#

