#================================#
import pygame as pg
import numpy as np
from random import choice
#================================#
from engine.configs.configs import configs
from engine.utils.log import log_error
#================================#
class Atlas:
    def __init__(self, error_image:pg.Surface):
        self.error_image = error_image
        #--------------------------------#
        self.data = {}
        #--------------------------------#
        self.error_already_happen = False
        self.error_image = error_image
        #--------------------------------#
        self.raycaster_textures = []
        self.raycaster_textures_ids = {} #key: id
        self.raycaster_texture_array = None
        #--------------------------------#
        self.save(f"{configs.engine.asset_marks.texture}@{configs.engine.acronym}::error", error_image)
        self.save(f"{configs.engine.asset_marks.raycast_texture}@{configs.engine.acronym}::error", error_image, is_raycaster=True)

    #================================#
    def save(self, name:str, image:pg.surface, is_raycaster=False):
        #--------------------------------#
        self.data[name] = image
        #--------------------------------#
        if is_raycaster:
            image = pg.transform.scale(image, (configs.game.raytexture_size, configs.game.raytexture_size))
            self.save_raycast(name, image)
    #================================#
    def save_raycast(self, name, surface):
        #--------------------------------#
        rgb = self.surface_to_rgb32(surface)
        #--------------------------------#
        self.raycaster_textures_ids[name] = len(self.raycaster_textures)
        #--------------------------------#
        self.raycaster_textures.append(rgb)
        #--------------------------------#
        self.raycaster_texture_array = np.asarray(
            self.raycaster_textures,
            dtype=np.uint32
        )
    #================================#
    def get_raytexture_id(self, name:str):
        #--------------------------------#
        id = self.raycaster_textures_ids.get(name)
        #--------------------------------#
        if id is None:
            log_error(f"Texture '{name}' not found as raytexture. Returning error texture id.", True)
            return self.raycaster_textures_ids[f"{configs.engine.asset_marks.raycast_texture}@{configs.engine.acronym}::error"]
        #--------------------------------#
        return id
    #--------------------------------#
    def get_raytexture(self, id:int):
        #--------------------------------#
        if -1 > id > len(self.raycaster_textures):
            log_error(f"Texture with id: '{id}' not found as raytexture. Returning error texture.", True)
            return
        #--------------------------------#
        return self.raycaster_textures[id]
    #--------------------------------#    
    def get_raytexture_by_name(self, name:str):
        #--------------------------------#
        id = self.get_raytexture_id(name)
        raytex = self.get_raytexture(id)
        #--------------------------------#
        return raytex
    #================================#
    def get(self, name:str):
        #--------------------------------#
        image = self.data.get(name)
        #--------------------------------#
        if not image:
            log_error(f"Sprite '{name}' not found in atlas. Returning error sprite.")#, True)
            return self.error_image
        #--------------------------------#
        return image
    #================================#
    def random(self):
        """
        Returns a random sprite from the atlas (debug purpose).
        """
        return choice(list(self.data.values()))
    #================================#
    @staticmethod
    def surface_to_rgb32(surface):

        arr = pg.surfarray.array3d(surface)

        arr = np.transpose(arr, (1,0,2))

        return (
            (arr[:,:,0].astype(np.uint32) << 16)
            | (arr[:,:,1].astype(np.uint32) << 8)
            | arr[:,:,2].astype(np.uint32)
        )

