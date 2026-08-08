import pygame as pg
import numpy as np
import math
#================================#
from engine.ecs.component_storage import register_engine_component
#--------------------------------#
from engine.utils.globalclasses import globalclasses
#================================#
@register_engine_component
class Texture:
    #--------------------------------#
    def __init__(self, texture:str, scale:tuple=None, convert_into_texture:bool=False):
        #--------------------------------#
        if convert_into_texture:
            self.texture = globalclasses.TextureHandler.get(texture)
        else:
            self.texture = texture
        self.original_texture = self.texture
        self.scale = scale
#================================#
@register_engine_component
class Position:
    def __init__(self,x,y):
        #--------------------------------#
        self.pos = pg.Vector2(x,y)
        self.old_pos = pg.Vector2(x,y)
    #--------------------------------#
    @property
    def x(self):
        return self.pos.x
    #--------------------------------#
    @x.setter
    def x(self,value):
        self.old_pos.x = self.pos.x
        self.pos.x = value
    #--------------------------------#
    @property
    def y(self):
        return self.pos.y
    #--------------------------------#
    @y.setter
    def y(self,value):
        self.old_pos.y = self.pos.y
        self.pos.y = value
#================================#
inf = float("inf")
@register_engine_component
class Velocity:
    #--------------------------------#
    def __init__(self, x:float, y:float, max_speed=[inf, inf], can_move:bool=True):
        #--------------------------------#
        self.max = pg.Vector2(*max_speed)
        self.vel = pg.Vector2(x,y)
        self.can_move = can_move
    #--------------------------------#
    @property
    def x(self):
        return self.vel.x
    #--------------------------------#
    @x.setter
    def x(self,value):
        self.vel.x = value
    #--------------------------------#
    @property
    def y(self):
        return self.vel.y
    #--------------------------------#
    @y.setter
    def y(self,value):
        self.vel.y = value
#================================#
@register_engine_component
class States:
    #--------------------------------#
    def __init__(self, initial:str, states:list[str]):
        #--------------------------------#
        self.initial = initial
        self.current = initial
        self.states = states
#================================#
@register_engine_component
class EntityType:
    def __init__(self, name: str):
        self.name = name
#================================#