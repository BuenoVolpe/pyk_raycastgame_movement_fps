import numpy as np
import math
import pygame as pg
#--------------------------------#
from engine.configs.configs import configs
from engine.utils.dict_to_class import dict_to_class
#--------------------------------#
from engine.signal_bus import signal_bus
from game.enums.signals import signals
from game.enums.signals_prioritys import sig_prio
#--------------------------------#
from engine.raycaster3D.constants import TEX_H, TEX_W, worldMap, default_sprites_data, default_thin_walls, default_doors, HIT_NONE
from engine.raycaster3D.map import Map
#--------------------------------#
from engine.raycaster3D.renderer.renderer_sprites import render_sprites
from engine.raycaster3D.renderer.walls_renderer import render_walls
from engine.raycaster3D.renderer.floor_ceiling_render import render_floor_ceiling
from engine.raycaster3D.renderer.pick_entity import pick_entity
#================================#
type array =  np.array
type array_surf =  np.array
type surface =  pg.Surface
#================================#
class RaycasterRenderer:
    #--------------------------------#
    def __init__(self):
        self.buffer = np.zeros((configs.game.raysurface_size[1], configs.game.raysurface_size[0]), dtype=np.uint32)  # screen buffer
        self.ZBuffer = np.zeros(configs.game.raysurface_size[0], dtype=np.float64)   # walls distance
        #--------------------------------#
        self.look_type = HIT_NONE
        self.look_index = -1
        self.look_eid = -1
        self.look_distance = 1e30
        #--------------------------------#
        self.map = Map()
    #--------------------------------#
    def render(self, textures, pos, dir, plane):
        #--------------------------------#
        self.buffer[:] = 0
        self.ZBuffer[:] = 1e30
        #--------------------------------#
        render_floor_ceiling(
            pos.x, pos.y,
            dir.x, dir.y,
            plane.x, plane.y,
            textures,
            self.buffer,
            self.ZBuffer,
            self.map.ceil_grid,
            self.map.floor_grid,
            floorDefaultTex1=self.map.floorDefaultTex1,
            floorDefaultTex2=self.map.floorDefaultTex2,
            ceilDefaultTex=self.map.ceilDefaultTex,
            TEX_W=TEX_W,
            TEX_H=TEX_H
        )
        #--------------------------------#
        render_walls(
            pos.x, pos.y,
            dir.x, dir.y,
            plane.x, plane.y,
            self.map.grid,
            textures,
            self.buffer,
            self.ZBuffer,
            self.map.thin_walls,
            self.map.doorsMap,
            TEX_W=TEX_W,
            TEX_H=TEX_H
        )
        #--------------------------------#
        render_sprites(
            pos.x, pos.y,
            dir.x, dir.y,
            plane.x, plane.y,
            self.sprites,
            textures,
            self.buffer,
            self.ZBuffer,
            TEX_W=TEX_W,
            TEX_H=TEX_H
        )
        #--------------------------------#
        self.look_type, self.look_index, self.look_eid, self.look_distance = pick_entity(
            pos.x,
            pos.y,
            dir.x,
            dir.y,
            plane.x,
            plane.y,
            self.map.grid,
            self.map.thin_walls,
            self.map.doorsMap,
            self.sprites,
            self.ZBuffer
        )

        return self.buffer
        #--------------------------------#

        