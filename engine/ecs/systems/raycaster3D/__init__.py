from engine.ecs.components.all import Camera3D, Direction, Angle, Position
from engine.configs.configs import configs
#--------------------------------#
from engine.utils.globalclasses import globalclasses
from engine.utils.dict_to_class import dict_to_class
#--------------------------------#
from engine.raycaster3D.constants import HIT_DOOR, HIT_NONE, HIT_SPRITE, HIT_THIN_WALL, HIT_WALL
#--------------------------------#
import math
import pygame as pg
import numpy as np
#================================#
class Raycast3DSystem:
    #--------------------------------#
    def __init__(self, world:object, renderer:object):
        #--------------------------------#
        self.world = world
        self.renderer = renderer
        #--------------------------------#
        self.on_screen = False
        self.do_render = configs.game.use_raycaster

    #================================#
    def update(self, surface):
        #--------------------------------#
        if not self.do_render:
            return
        #--------------------------------#
        for ent, (angle, pos, direction, camera) in self.world.query(Angle, Position, Direction, Camera3D):
            #-------------------------------------#
            frame = self.renderer.render(
                globalclasses.TextureHandler.atlas.raycaster_texture_array,
                pos.pos,
                direction.dir,
                camera.plane
            )
            #-------------------------------------#
            look_type = self.renderer.look_type
            look_index = self.renderer.look_index
            look_eid = self.renderer.look_eid
            look_distance = self.renderer.look_distance

            #-------------------------------------#
            frame_surface = buffer_to_surface(frame)
            surface.blit(frame_surface, configs.game.raysurf_pos)
            #-------------------------------------#

#================================#
def buffer_to_surface(buffer_uint32):
    """
    Convert uint32 buffer (0xRRGGBB) to Pygame Surface
    """
    r = ((buffer_uint32 >> 16) & 0xFF).astype(np.uint8)
    g = ((buffer_uint32 >> 8) & 0xFF).astype(np.uint8)
    b = (buffer_uint32 & 0xFF).astype(np.uint8)
    rgb = np.dstack((r,g,b))
    rgb_t = np.transpose(rgb, (1,0,2))  # Pygame espera (w,h,3)
    surf = pg.surfarray.make_surface(rgb_t)
    return surf



