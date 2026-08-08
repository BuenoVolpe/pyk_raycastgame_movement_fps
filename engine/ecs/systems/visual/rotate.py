from engine.ecs.components.all import LookAt, Angle, Position, Texture, RotateTextureTag
from engine.utils.scaler import scaler
from engine.utils.globalclasses import globalclasses
from engine.configs.configs import configs
#================================#
import pygame as pg
import math
#================================#
class LookAtSystem:
    #--------------------------------#
    def __init__(self, world):
        self.world = world
    #================================#
    def update(self, dt):
        #--------------------------------#
        x,y = pg.mouse.get_pos()
        mouse_pos = x+globalclasses.Camera.x, y+globalclasses.Camera.y
        #--------------------------------#
        for entity, (look, pos, rotation) in self.world.query(LookAt, Position, Angle):
            #--------------------------------#
            # cooldown
            if look.change_timer > 0:
                look.change_timer -= dt
                continue
            #--------------------------------#
            target = self.find_target(
                entity,
                look,
                pos,
                mouse_pos
            )
            #--------------------------------#
            if target is None:
                continue
            #--------------------------------#
            look.current_target = target
            #--------------------------------#
            target_pos = self.get_target_position(target)
            #--------------------------------#
            if target_pos is None:
                continue
            #--------------------------------#
            dx = target_pos[0] - pos.x
            dy = target_pos[1] - pos.y
            #--------------------------------#
            rotation.angle = math.degrees(math.atan2(dy, dx))
            #--------------------------------#
            if look.change_cooldown >= 0:
                look.change_timer = look.change_cooldown

    #--------------------------------#
    def find_target(self, entity, look, pos, mouse):
        #--------------------------------#
        possible = []
        #--------------------------------#
        for target_type in look.targets:
            #--------------------------------#
            # mouse especial
            if target_type == "mouse":
                possible.append(
                    ("mouse", mouse)
                )
                continue
            #--------------------------------#
            # entidades
            for target, _ in self.world.get_entities_with_type(target_type):
                #--------------------------------#
                if target == entity:
                    continue
                #--------------------------------#
                target_pos = self.world.get_component(
                    target,
                    Position
                )
                #--------------------------------#
                if target_pos:
                    #--------------------------------#
                    possible.append(
                        (
                            #--------------------------------#
                            target,
                            (
                                target_pos.x,
                                target_pos.y
                            )
                        )
                    )
        #--------------------------------#
        if not possible:
            return None
        #--------------------------------#
        if look.focus == "nearest":
            #--------------------------------#
            return min(
                possible,
                key=lambda t:
                    self.distance(
                        pos.x,
                        pos.y,
                        t[1][0],
                        t[1][1]
                    )
            )
        #--------------------------------#
        return possible[0]
    #--------------------------------#
    def get_target_position(self, target):
        #--------------------------------#
        # mouse
        if target[0] == "mouse":
            return target[1]
        #--------------------------------#
        # entidade
        entity = target[0]
        #--------------------------------#
        pos = self.world.get_component(
            entity,
            Position
        )
        #--------------------------------#
        if pos:
            return (
                pos.x,
                pos.y
            )
        #--------------------------------#
        return None
    #--------------------------------#
    def distance(self, x1, y1, x2, y2):
        #--------------------------------#
        return math.sqrt(
            (x2 - x1) ** 2 +
            (y2 - y1) ** 2
        )
#================================#
class VisualRotationSystem:
    #--------------------------------#
    def __init__(self, world):
        self.world = world
    #================================#
    def update(self, dt):
        #--------------------------------#
        #--------------------------------#
        for entity, (tex, rot, tag) in self.world.query(Texture, Angle, RotateTextureTag):
            #--------------------------------#
            tex.texture = pg.transform.rotate(tex.original_texture, -rot.angle)

