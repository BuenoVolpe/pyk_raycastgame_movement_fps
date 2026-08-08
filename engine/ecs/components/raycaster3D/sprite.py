import pygame as pg
import numpy as np
import math
#================================#
from engine.ecs.component_storage import register_engine_component
#--------------------------------#
from engine.utils.globalclasses import globalclasses
#================================#
@register_engine_component
class Scale3D:
    def __init__(self, scale=1):
        self.scale = scale
#================================#
@register_engine_component
class OffsetZ3D:
    def __init__(self, offsetZ=0):
        self.offsetZ = offsetZ
#================================#