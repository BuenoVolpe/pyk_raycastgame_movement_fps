
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
#================================#
type array =  np.array
type array_surf =  np.array
type surface =  pg.Surface
#================================#
class Map:
    def __init__(self):
        self.thin_walls = default_thin_walls
        self.sprites = default_sprites_data
        self.sprites_list = list(default_sprites_data)
        self.doorsMap = default_doors
        self.grid = worldMap
        self.ceil_grid = worldMap
        self.floor_grid = worldMap
        self.floorDefaultTex1 = 1
        self.floorDefaultTex2 = 2
        self.ceilDefaultTex = 3
        #--------------------------------#
        signal_bus.subscribe(signals.SET_RAYMAP, self.set_map, priority=sig_prio.LOAD)
        signal_bus.subscribe(signals.SET_RAYMAP_DOOR, self.set_door, priority=sig_prio.LOAD)
        #--------------------------------#
    def set_map(self, thin_walls:array=None, sprites:array=None, doorsMap:array=None, grid:array=None, ceil_grid:array=None, floor_grid:array=None, floorDefaultTex1:int=None, floorDefaultTex2:int=None, ceilDefaultTex:int=None):
        #--------------------------------#
        self.thin_walls = thin_walls if thin_walls is not None else default_thin_walls
        self.sprites_list = sprites if sprites is not None else default_sprites_data
        self.sprites = np.array(self.sprites_list, dtype=np.float64)
        self.doorsMap = doorsMap if doorsMap is not None else default_doors
        #--------------------------------#
        self.grid = grid if grid is not None else worldMap
        self.ceil_grid = ceil_grid if ceil_grid is not None else worldMap
        self.floor_grid = floor_grid if floor_grid is not None else worldMap
        #--------------------------------#
        self.floorDefaultTex1 = floorDefaultTex1 if floorDefaultTex1 is not None else 1
        self.floorDefaultTex2 = floorDefaultTex2 if floorDefaultTex2 is not None else 2
        self.ceilDefaultTex = ceilDefaultTex if ceilDefaultTex is not None else 3
        #--------------------------------#
        signal_bus.emit(signals.GRID_COLLISION_CHANGE_GRID, new_grid=self.grid, thin_walls=self.thin_walls, doors=self.doorsMap)

    def set_door(self, index, 
                 x=None,y=None,direction=None,length=None,texture=None,offset=None,speed=None,open_state=None,has_jamb=None,jamb_texture=None,eid=None):
        self.doorsMap[index, 0] = x or self.doorsMap[index, 0] 
        self.doorsMap[index, 1] = y or self.doorsMap[index, 1] 
        self.doorsMap[index, 2] = direction or self.doorsMap[index, 2] 
        self.doorsMap[index, 3] = length or self.doorsMap[index, 3] 
        self.doorsMap[index, 4] = texture or self.doorsMap[index, 4] 
        self.doorsMap[index, 5] = offset or self.doorsMap[index, 5] 
        self.doorsMap[index, 6] = speed or self.doorsMap[index, 6] 
        self.doorsMap[index, 7] = open_state or self.doorsMap[index, 7] 
        self.doorsMap[index, 8] = has_jamb or self.doorsMap[index, 8] 
        self.doorsMap[index, 9] = jamb_texture or self.doorsMap[index, 9] 
        self.doorsMap[index, 10] = eid or self.doorsMap[index, 10] 

