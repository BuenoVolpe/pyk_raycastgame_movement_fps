import pygame as pg
import numpy as np
import math
#================================#
from engine.ecs.component_storage import register_engine_component
#--------------------------------#
from engine.utils.globalclasses import globalclasses
#================================#
@register_engine_component
class GridCollider:
    def __init__(self, radius=0.2):
        self.radius = radius
#================================#

