from operator import pos

from engine.ecs.components.all import Position, ThinWall3DTag
from engine.utils.globalclasses import globalclasses
from engine.utils.overlay import debug_overlay
from game.enums.assets_marks import assetsmarks
from engine.raycaster3D.constants import HIT_NONE, HIT_WALL, HIT_THIN_WALL, HIT_DOOR, HIT_SPRITE, default_thin_walls
from engine.signal_bus import signal_bus
from game.enums.signals import signals
from game.enums.signals_prioritys import sig_prio
import pygame as pg
import math
#================================#
class ThinWallUpdateSystem:
    #================================#
    def __init__(self, world):
        #--------------------------------#
        self.world = world
        #--------------------------------#
        self.thin_walls = default_thin_walls
        #--------------------------------#
        signal_bus.subscribe(signals.SET_RAYMAP, self.set_thin_walls, priority=sig_prio.LOAD)
    #================================#
    def set_thin_walls(self, thin_walls, **kwargs):
        self.thin_walls = thin_walls if thin_walls is not None else default_thin_walls
    #================================#
    def update(self, dt):
        #--------------------------------#
        for i in range(self.thin_walls.shape[0]):
            #--------------------------------#
            x,y = self.thin_walls[i,0], self.thin_walls[i,1]
            eid = self.thin_walls[i, 6]
            #--------------------------------#
            if eid == -1:
                for i in range(self.thin_walls.shape[0]):
                    for eid, (pos, thin_wall) in self.world.query(Position, ThinWall3DTag):
                        if pos.x == x and pos.y == y:
                            thin_wall[i, 6] = eid
            
