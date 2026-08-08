import os
import pygame as pg
import numpy as np
#=====================================#
from engine.utils.recolor import recolor
from engine.utils.json import scan_folder_with_json
from engine.utils.scaler import scaler
from engine.utils.log import log_list, log_error
#=====================================#
from engine.configs.configs import configs
#=====================================#
from game.enums.assets_marks import assetsmarks
#=====================================#
pg.init()
#=====================================#
class Loader:
    def __init__(self, atlas:object, image_loader:object, paths:object, color_map:dict):
        #-------------------------------------#
        self.engine_path = getattr(paths, configs.engine.acronym)
        self.game_path = getattr(paths, configs.game.acronym)
        #-------------------------------------#
        self.paths = {
            configs.engine.acronym: self.engine_path,
            configs.game.acronym: self.game_path
        }
        #-------------------------------------#
        self.atlas = atlas
        self.image_loader = image_loader
        #-------------------------------------#
        self.color_map = color_map
        #-------------------------------------#
        self._load()
        #-------------------------------------#
        # log_list(list(self.atlas.data.keys()))
    #=====================================#
    def _load(self):
        #-------------------------------------#
        engine_asset = assetsmarks.engine.texture
        ray_engine_asset = assetsmarks.engine.raycast_texture
        game_asset = assetsmarks.game.texture
        ray_game_asset = assetsmarks.game.raycast_texture
        #=====================================#
        for base, path in self.paths.items():
            for info in scan_folder_with_json(path, extension=f".{configs.engine.extensions.texture}"):
                #--------------------------------#
                name = info["name"]
                image_path = info["file_path"]
                json_path = info["json_path"]
                meta = info["metadata"]
                #--------------------------------#
                convert_alpha = meta.get("convert_alpha", True)
                use_colorkey = meta.get("use_colorkey", False)
                is_raycaster = meta.get("is_raycaster")
                type = meta.get("type")
                colors = meta.get("colors")
                scale = meta.get("scale")
                use_constant = meta.get("use_constant", False)
                #=====================================#
                sprite = self.image_loader.load(
                    image_path,
                    convert_alpha,
                    use_colorkey
                )
                #=====================================#
                atlas_path = os.path.relpath(image_path, path)
                atlas_path = atlas_path.replace(f".{configs.engine.extensions.texture}", "").replace("\\", ".")
                #-------------------------------------#
                if base == configs.engine.acronym:
                    mark=engine_asset
                elif base == configs.game.acronym:
                    mark=game_asset
                if configs.game.use_raycaster and (atlas_path.startswith(configs.engine.raytexture_folder) or is_raycaster): 
                    is_raycaster = True
                    mark = ray_engine_asset if mark == engine_asset else ray_game_asset
                #-------------------------------------#
                atlas_path = f"{mark}::{atlas_path}"
                #=====================================#
                if type == "sheet":
                    self._load_sheet(sprite, meta, self.color_map, atlas_path, is_raycaster)
                    continue
                if colors:
                    self.recolor_sprite(sprite, colors, atlas_path, self.color_map, meta, is_raycaster)
                    continue
                if scale:
                    sprite = scaler.surface(sprite, scale, use_constant)
                #-------------------------------------#
                self.atlas.save(atlas_path, sprite, is_raycaster)

    #=====================================#
    def _load_sheet(self, sheet: pg.Surface, meta: dict, color_maps: dict, atlas_path: str, is_raycaster=False):
        #-------------------------------------#
        self.atlas.save(atlas_path, sheet)
        #=====================================#
        meta = meta.copy()
        #--------------------------------#
        if sprites := meta.get("sprites"):
            for sprite_name, sprite in sprites.items():
                #--------------------------------#
                start = sprite.get("start",[0,0])
                size = sprite.get("size",[1,1])
                #--------------------------------#
                convert_alpha = sprite.get("convert_alpha", True)
                use_colorkey = sprite.get("use_colorkey", False)
                type = sprite.get("type")
                colors = sprite.get("colors")
                scale = sprite.get("scale")
                use_constant = sprite.get("use_constant", False)
                #--------------------------------#
                image = sheet.subsurface(pg.Rect(start, size))
                #--------------------------------#
                sprite_atlas_path = f"{atlas_path}::{sprite_name}"
                #--------------------------------#
                if colors:
                    self.recolor_sprite(image, colors, sprite_atlas_path, color_maps, sprite)
                #--------------------------------#
                if scale:
                    image = scaler.surface(image, scale, use_constant)
                #--------------------------------#
                self.atlas.save(sprite_atlas_path, image, is_raycaster)

        #-------------------------------------#
        if sprites is None:
            log_error(f"no sprites found in sheet {atlas_path}", True)

    def recolor_sprite(self, sprite:pg.Surface, colors:list, atlas_path:str, color_maps:dict, meta:dict={}, is_raycaster=False):
        #--------------------------------#
        sprite_ = sprite
        if scale := meta.get("scale"):
            sprite_ = scaler.surface(sprite, scale, meta.get("use_constant", False))
        #--------------------------------#
        self.atlas.save(atlas_path, sprite_, is_raycaster)
        self.atlas.save(f"{atlas_path}.standart", sprite_, is_raycaster)
        #--------------------------------#
        for color in colors:
            #--------------------------------#
            sprite_copy = sprite.copy()
            #--------------------------------#
            if color not in color_maps:
                log_error(f"Color map '{color}' specified for '{atlas_path}' not found in color maps.")#, console)
                continue
            #--------------------------------#
            sprite_copy = recolor(sprite_copy, color_maps[color])
            #--------------------------------#
            if scale := meta.get("scale"):
                sprite_copy = scaler.surface(sprite_copy, scale, meta.get("use_constant", False))
            #--------------------------------#
            self.atlas.save(f"{atlas_path}.{color}", sprite_copy, is_raycaster)

    #=====================================#
    def set_texture_to_correct_size(self, sprite):
        #--------------------------------#
        texture = self.get(sprite)
        texture_size = configs.engine.raytexture_size
        #--------------------------------#
        resized_sprite = pg.transform.scale(texture, [texture_size, texture_size])
        self.atlas.save(sprite, resized_sprite)
        return resized_sprite
    
