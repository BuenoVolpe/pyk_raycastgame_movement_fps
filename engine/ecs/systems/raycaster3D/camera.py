from engine.ecs.components.all import Camera3D, Direction, Angle, MouseSentibility, PlayerTag, LookingAtEntity
from engine.utils.globalclasses import globalclasses
from engine.utils.overlay import debug_overlay
from game.enums.assets_marks import assetsmarks
from engine.raycaster3D.constants import HIT_NONE, HIT_WALL, HIT_THIN_WALL, HIT_DOOR, HIT_SPRITE
import pygame as pg
import math
#================================#
class Raycaster3DCameraSystem:
    #--------------------------------#
    def __init__(self, world:object):
        #--------------------------------#
        self.world = world

    #================================#
    def update(self, dt):
        #--------------------------------#
        for ent, (angle, direction, camera) in self.world.query(Angle, Direction, Camera3D):
            #--------------------------------#
            rad = math.radians(angle.angle)

            direction.x = math.cos(rad)
            direction.y = math.sin(rad)
            #--------------------------------#
            plane_len = math.tan(math.radians(camera.fov) / 2)

            camera.plane.x = -direction.y * plane_len
            camera.plane.y = direction.x * plane_len
#================================#
class MouseLookSystem:
    #--------------------------------#
    def __init__(self, world):
        #--------------------------------#
        self.world = world
        #--------------------------------#
        pg.mouse.get_rel()
    #--------------------------------#
    def update(self, dt):
        #--------------------------------#
        dx, dy = pg.mouse.get_rel()
        #--------------------------------#
        for ent, (angle, sens) in self.world.query(Angle,MouseSentibility):
            #--------------------------------#
            angle.angle += dx * sens.sentibility
            #--------------------------------#
            angle.angle %= 360        
#================================#
class LookingAtEntitySystem:
    #--------------------------------#
    def __init__(self, world):
        #--------------------------------#
        self.world = world
        #--------------------------------#
        debug_overlay.watch(
            f"{assetsmarks.engine.debug}::overlay.looking_at_looking_at_eid",
            lambda: (globalclasses.RaycasterRenderer.look_eid)
        )
        debug_overlay.watch(
            f"{assetsmarks.engine.debug}::overlay.looking_at_looking_at_type",
            lambda: (get_look_type())
        )
        debug_overlay.watch(
            f"{assetsmarks.engine.debug}::overlay.looking_at_looking_at_index",
            lambda: (globalclasses.RaycasterRenderer.look_index)
        )
        debug_overlay.watch(
            f"{assetsmarks.engine.debug}::overlay.looking_at_looking_at_distance",
            lambda: (f"{globalclasses.RaycasterRenderer.look_distance:.2f}")
        )
    #--------------------------------#
    def update(self, dt):
        #--------------------------------#
        for ent, (looking_at, ptag, ctag) in self.world.query(LookingAtEntity,PlayerTag,Camera3D):
            #--------------------------------#
            looking_at.eid = globalclasses.RaycasterRenderer.look_eid
            looking_at.index = globalclasses.RaycasterRenderer.look_index
            looking_at.distance = globalclasses.RaycasterRenderer.look_distance
            looking_at.type = globalclasses.RaycasterRenderer.look_type
            #--------------------------------#            
#================================#

def get_look_type():
    #--------------------------------#            
    type = globalclasses.RaycasterRenderer.look_type
    #--------------------------------#          
    if type == HIT_WALL:
        type_str = "Wall"
    #--------------------------------#          
    elif type == HIT_THIN_WALL:
        type_str = "Thin_Wall"
    #--------------------------------#          
    elif type == HIT_DOOR:
        type_str = "Door"
    #--------------------------------#          
    elif type == HIT_SPRITE:
        type_str = "Sprite"
    #--------------------------------#          
    else:
        type_str = "None"
    #--------------------------------#          
    return type_str
