



import pygame as pg
import numpy as np
import math
#================================#
from engine.ecs.component_storage import register_engine_component
#--------------------------------#
from engine.utils.globalclasses import globalclasses
#================================#
@register_engine_component
class Tag:
    def __init__(self, **tags):
        #--------------------------------#
        for name, value in tags.items():
            setattr(self, name.upper(), value)
#================================#
@register_engine_component
class CameraFocusTag(Tag):
    #--------------------------------#
    def __init__(self, **tags):
        self.IS_CAMERA_FOCUS = True
        #--------------------------------#
        super().__init__(**tags)
#================================#
@register_engine_component
class PlayerTag(Tag):
    #--------------------------------#
    def __init__(self, **tags):
        self.IS_PLAYER = True
        #--------------------------------#
        super().__init__(**tags)
#================================#
@register_engine_component
class NoClipTag(Tag):
    #--------------------------------#
    def __init__(self, **tags):
        self.NOCLIP = True
        #--------------------------------#
        super().__init__(**tags)
#================================#
@register_engine_component
class AngularMovementTag(Tag):
    #--------------------------------#
    def __init__(self, **tags):
        self.DO_ANGULAR_MOVEMENT = True
        #--------------------------------#
        super().__init__(**tags)
#================================#
@register_engine_component
class CollisionTag(Tag):
    #--------------------------------#
    def __init__(self, **tags):
        self.DO_COLLISION = True
        #--------------------------------#
        super().__init__(**tags)
#================================#
@register_engine_component
class RotateTextureTag(Tag):
    #--------------------------------#
    def __init__(self, **tags):
        self.DO_ROTATE_TEXTURE = True
        #--------------------------------#
        super().__init__(**tags)
#================================#
@register_engine_component
class Sprite3DTag(Tag):
    #--------------------------------#
    def __init__(self, **tags):
        self.IS_SPRITE3D = True
        self.sid = None
        #--------------------------------#
        super().__init__(**tags)
#================================#
@register_engine_component
class Door3DTag(Tag):
    #--------------------------------#
    def __init__(self, **tags):
        self.IS_DOOR3D = True
        self.did = None
        #--------------------------------#
        super().__init__(**tags)
#================================#
@register_engine_component
class ThinWall3DTag(Tag):
    #--------------------------------#
    def __init__(self, **tags):
        self.IS_THINWALL3D = True
        self.twid = None
        #--------------------------------#
        super().__init__(**tags)

