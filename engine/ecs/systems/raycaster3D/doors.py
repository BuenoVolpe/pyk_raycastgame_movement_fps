from operator import pos

from engine.ecs.components.all import Position, Door
from engine.utils.globalclasses import globalclasses
from engine.utils.overlay import debug_overlay
from game.enums.assets_marks import assetsmarks
from engine.raycaster3D.constants import HIT_NONE, HIT_WALL, HIT_THIN_WALL, HIT_DOOR, HIT_SPRITE, default_doors
from engine.signal_bus import signal_bus
from game.enums.signals import signals
from game.enums.signals_prioritys import sig_prio
import pygame as pg
import math
#================================#
class DoorUpdateSystem:
    #--------------------------------#
    CLOSED = 0
    CLOSING = 1
    OPEN = 2
    OPENING = 3
    LOCKED = 4
    OPEN_FORCE = 5
    #================================#
    def __init__(self, world):
        #--------------------------------#
        self.world = world
        #--------------------------------#
        self.doors = default_doors
        #--------------------------------#
        signal_bus.subscribe(signals.SET_RAYMAP, self.set_doors, priority=sig_prio.LOAD)
        signal_bus.subscribe(signals.INTERACT, self.toggle_door, priority=sig_prio.UPDATE_OBJ)
    #================================#
    def set_doors(self, doorsMap, **kwargs):
        self.doors = doorsMap if doorsMap is not None else doorsMap
    #================================#
    def update(self, dt):
        #--------------------------------#
        for i in range(self.doors.shape[0]):
            #--------------------------------#
            x,y = self.doors[i,0], self.doors[i,1]
            offset = self.doors[i, 5]
            speed = self.doors[i, 6]
            state = int(self.doors[i, 7])
            eid = int(self.doors[i, 10])
            #--------------------------------#
            if eid == -1:
                for i in range(self.doors.shape[0]):
                    x, y = self.doors[i, 0], self.doors[i, 1]
                    for eid, (pos, door) in self.world.query(Position, Door):
                        if pos.x == x and pos.y == y:
                            door[i, 10] = eid
            #--------------------------------#
            if state == self.OPENING:
                offset += speed * dt
                if offset >= 0.9:
                    offset = 1
                    state = self.OPEN
            elif state == self.CLOSING:
                px, py = self.world.get_player()[1]["Position"].pos  # você precisa passar isso

                if abs(px - x) < 0.5 and abs(py - y) < 0.5:
                    continue  # não fecha

                offset -= speed * dt
                if offset <= 0.0:
                    offset = 0.0
                    state = self.CLOSED
            #--------------------------------#
            signal_bus.emit(signals.SET_RAYMAP_DOOR, index=i, x=x, y=y, offset=offset, speed=speed, open_state=state, eid=eid)
            #--------------------------------#
            door_comp = self.world.get_entity_components(eid).get("Door")
            door_tag = self.world.get_entity_components(eid).get("Door3DTag")
            if door_comp:
                door_tag.did = i
                door_comp.state = state
                door_comp.offset = offset
                door_comp.speed = speed
    #================================#
    def toggle_door(self, player_eid, player_comps, **kwargs):
        ent = player_comps["LookingAtEntity"]
        #--------------------------------#
        type = ent.type
        index = ent.index
        eid = ent.eid
        distance = ent.distance
        #--------------------------------#
        if index == -1: return
        if type != HIT_DOOR: return
        if distance > 2.0: return
        #--------------------------------#
        state = int(self.doors[index, 7])
        eid = int(self.doors[index, 10])
        #--------------------------------#
        if state in (self.OPEN, self.OPENING):
            state = self.CLOSING
        #--------------------------------#
        elif state in (self.CLOSED, self.CLOSING):
            state = self.OPENING
        #--------------------------------#
        signal_bus.emit(signals.SET_RAYMAP_DOOR, index=index, open_state=state)
        door_comp = self.world.get_entity_components(eid)["Door"]
        door_comp.state = state


def can_open_door(cam, door):
    dx = door[0] - cam.pos[0]
    dy = door[1] - cam.pos[1]

    dist = math.sqrt(dx*dx + dy*dy)
    if dist > 2.0:
        return False

    # normaliza
    dx /= dist
    dy /= dist

    # dot product
    dot = dx * cam.dir[0] + dy * cam.dir[1]

    return dot > 0.5  # ~60° cone

