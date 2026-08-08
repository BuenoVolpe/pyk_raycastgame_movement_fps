import pygame as pg
import numpy as np
import math
#================================#
from engine.ecs.component_storage import register_engine_component
#--------------------------------#
from engine.utils.globalclasses import globalclasses
#================================#
@register_engine_component
class Inputs:
    #--------------------------------#
    def __init__(self, inputs:list):
        #--------------------------------#
        self.inputs = {}
        #--------------------------------#
        for name in inputs:
            self.inputs[name] = False
            setattr(self, name, False)
    #================================#
    def _reload(self, *new_inputs):
        #--------------------------------#
        for name in self.inputs.keys():
            setattr(self, name, self.inputs[name])
        #--------------------------------#
        for name in new_inputs:
            self.inputs[name] = self.inputs.get(name, False)
            setattr(self, name, self.inputs[name])
#================================#