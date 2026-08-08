from engine.ecs.components.all import Texture, Scale3D, OffsetZ3D, Sprite3DTag, Position
from engine.configs.configs import configs
#--------------------------------#
from engine.utils.globalclasses import globalclasses
from engine.utils.dict_to_class import dict_to_class
#--------------------------------#
import math
import pygame as pg
import numpy as np
#================================#
class Sprites3DSystem:
    #--------------------------------#
    def __init__(self, world:object):
        #--------------------------------#
        self.world = world
        #--------------------------------#
        self.do_render = configs.game.use_raycaster
    #================================#
    def update(self, surface):
        #--------------------------------#
        if not self.do_render:
            return
        #================================#
        for entity, (pos, tex, scale, offsetZ, tag) in globalclasses.World.query(Position, Texture, Scale3D, OffsetZ3D, Sprite3DTag):
            #--------------------------------#
            sprites_list = globalclasses.RaycasterRenderer.map.sprites_list
            was_created = False
            #-------------------------------------#
            for sid, sprinfo in enumerate(sprites_list.copy()):
                if sprinfo[5] == entity:
                    was_created = True
                    break
            #================================#
            tex.texture = globalclasses.TextureHandler.get_raytexture_id(tex.texture) if isinstance(tex.texture, str) else tex.texture
            #-------------------------------------#
            sprinfo = [
                pos.x, pos.y,
                tex.texture,
                scale.scale,
                offsetZ.offsetZ,
                entity
            ]
            #================================#
            if not was_created:
                #-------------------------------------#
                sprites_list.append(sprinfo)            
                continue
            #================================#
            sprites_list[sid] = sprinfo
        #-------------------------------------#
        globalclasses.RaycasterRenderer.sprites_list = sprites_list
        globalclasses.RaycasterRenderer.sprites = np.array(sprites_list, dtype=np.float64)
        

            




