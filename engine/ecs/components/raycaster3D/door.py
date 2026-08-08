import pygame as pg
import numpy as np
import math
#================================#
from engine.ecs.component_storage import register_engine_component
#--------------------------------#
from engine.utils.globalclasses import globalclasses
#================================#
@register_engine_component
class Door:
    def __init__(self, direction=1, length=1, offset=0, speed=1, open_state=0, has_jamb=False):
        self.direction = direction
        self.length = length
        self.offset = offset
        self.speed = speed
        self.open_state = open_state
        self.has_jamb = has_jamb

