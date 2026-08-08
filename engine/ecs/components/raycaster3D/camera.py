import pygame as pg
import numpy as np
import math
#================================#
from engine.ecs.component_storage import register_engine_component
#--------------------------------#
from engine.utils.globalclasses import globalclasses
#================================#
@register_engine_component
class Direction:
    def __init__(self, x=1.0, y=0.0):
        self.dir = pg.Vector2(x, y)

    @property
    def x(self):
        return self.dir.x

    @x.setter
    def x(self, value):
        self.dir.x = value

    @property
    def y(self):
        return self.dir.y

    @y.setter
    def y(self, value):
        self.dir.y = value
#================================#
@register_engine_component
class MouseSentibility:
    def __init__(self, sentibility:float):
        self.sentibility = sentibility
#================================#
@register_engine_component
class Camera3D:
    def __init__(self, fov=90):
        self.fov = fov
        #--------------------------------#
        self.dir = pg.Vector2()
        self.plane = pg.Vector2()
        #--------------------------------#
        self.update_vectors(0)

    #================================#
    def update_vectors(self, angle_deg):
        #--------------------------------#
        angle = math.radians(angle_deg)
        #--------------------------------#
        self.dir.x = math.cos(angle)
        self.dir.y = math.sin(angle)
        #--------------------------------#
        plane_len = math.tan(math.radians(self.fov) / 2)
        #--------------------------------#
        self.plane.x = -self.dir.y * plane_len
        self.plane.y = self.dir.x * plane_len
#================================#
@register_engine_component
class LookingAtEntity:
    def __init__(self, eid:int=-1):
        self.type = 0
        self.index = -1
        self.eid = -1
        self.distance = 1e30


    # def set_eid(self, eid:int):
    #     self.eid = eid

