import pygame as pg
import numpy as np
import math
#================================#
from engine.ecs.component_storage import register_engine_component
#--------------------------------#
from engine.utils.globalclasses import globalclasses
#================================#
@register_engine_component
class LookAt:
    #--------------------------------#
    def __init__(self, targets=[], focus="nearest", change_cooldown=-1):
        #--------------------------------#
        self.targets = targets
        #--------------------------------#
        self.focus = focus
        #--------------------------------#
        self.current_target = None
        #--------------------------------#
        self.change_cooldown = change_cooldown
        self.do_change = False
        self.change_timer = 0
#================================#
@register_engine_component
class Angle:
    #--------------------------------#
    def __init__(self, angle:float):
        #--------------------------------#
        self.angle = angle
#================================#