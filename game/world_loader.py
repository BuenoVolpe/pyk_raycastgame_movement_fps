import random
import os
import copy
import numpy as np
#=====================================#
from engine.utils.json import json_reader, scan_folder_for_json
from engine.utils.debug_log import debug_log
from engine.utils.overlay import debug_overlay
from engine.utils.globalclasses import globalclasses
from engine.utils.log import log_error
from engine.utils.map_creator import map_create, mapping
# from engine.utils.dict_to_class import dict_to_class
from engine.raycaster3D.constants import worldMap_list, sprites
#-------------------------------------#
from engine.ecs.components.all import Position, Texture, Sprite3DTag, Scale3D, OffsetZ3D
#-------------------------------------#
from engine.configs.configs import configs
#-------------------------------------#
from engine.signal_bus import signal_bus
from game.enums.signals import signals
from game.enums.signals_prioritys import signals_prioritys
from game.enums.assets_marks import assetsmarks
#=====================================#
class WorldLoader:
    def __init__(self):
        #-------------------------------------#
        signal_bus.subscribe(signals.LOAD_COMPLETE_WORLD, self.load_world, priority=signals_prioritys.LOAD)
    #=====================================#
    def load_world(self, name:str, data:dict):
        self.texture_handler = globalclasses.TextureHandler
        #-------------------------------------#
        map_info = data.get("map_info", {})
        mapping = data.get("mapping", {})
        #=====================================#
        if not map_info:
            #-------------------------------------#
            log_error("map_info not found using default map_info")
            signal_bus.emit(signals.SET_RAYMAP)
        else:
            self.load_ray_map(map_info, mapping)
    #=====================================#
    def load_ray_map(self, map_info:dict, mapping:dict):
        #-------------------------------------#
        mapping = self.make_mapping(mapping)
        #-------------------------------------#
        grid = map_info.get("grid")
        grid = self.make_grid(grid, mapping)
        #-------------------------------------#
        ceil_grid = map_info.get("ceil_grid")
        ceil_grid = self.make_grid(ceil_grid, mapping)
        #-------------------------------------#
        floor_grid = map_info.get("floor_grid")
        floor_grid = self.make_grid(floor_grid, mapping)
        #-------------------------------------#
        thin_walls = map_info.get("thin_walls")
        thin_walls = self.make_thin_walls(thin_walls)
        #-------------------------------------#
        sprites = map_info.get("sprites")
        sprites = self.make_sprites(sprites)
        #-------------------------------------#
        doorsMap = map_info.get("doors")
        doorsMap, thin_walls = self.make_doors(doorsMap, thin_walls)
        #-------------------------------------#
        floorDefaultTex1 = map_info.get("floorDefaultTex1", 0)
        floorDefaultTex2 = map_info.get("floorDefaultTex2", 0)
        ceilDefaultTex = map_info.get("ceilDefaultTex", 0)
        #=====================================#
        if floorDefaultTex1:
            floorDefaultTex1 = self.texture_handler.get_raytexture_id(str(floorDefaultTex1))
        if floorDefaultTex2:
            floorDefaultTex2 = self.texture_handler.get_raytexture_id(str(floorDefaultTex2))
        if ceilDefaultTex:
            ceilDefaultTex = self.texture_handler.get_raytexture_id(str(ceilDefaultTex))
        #=====================================#
        signal_bus.emit(
            signals.SET_RAYMAP, 
            #-------------------------------------#
            grid = np.array(grid, dtype=np.int32),
            #-------------------------------------#
            floorDefaultTex1 = floorDefaultTex1,
            floorDefaultTex2 = floorDefaultTex2,
            ceilDefaultTex = ceilDefaultTex,
            #-------------------------------------#
            thin_walls = thin_walls,
            doorsMap = doorsMap,
            sprites = sprites,
            #-------------------------------------#
            ceil_grid = np.array(ceil_grid, dtype=np.int32),
            floor_grid = np.array(floor_grid, dtype=np.int32),
            #-------------------------------------#
            )
    #=====================================#
    def make_mapping(self, mapping:dict):
        #-------------------------------------#
        for key, value in mapping.items():
            if isinstance(value, str):
                mapping[key] = self.texture_handler.get_raytexture_id(value)
        #-------------------------------------#
        return mapping
    #=====================================#
    def make_grid(self, grid:list[list], mapping:dict):
        #-------------------------------------#
        if isinstance(grid, str):
            raise NotImplementedError
        #-------------------------------------#
        if grid is None:
            grid = worldMap_list
        #-------------------------------------#
        for y,line in enumerate(grid.copy()):
            for x,value in enumerate(line):
                #-------------------------------------#
                if isinstance(value, int):
                    value = str(value)                    
                if value in mapping:
                    grid[y][x] = mapping[value]
        #-------------------------------------#
        return grid
    #=====================================#
    def make_thin_walls(self, thin_walls:list[dict]):
        #-------------------------------------#
        if thin_walls is None:
            return np.empty((0, 7), dtype=np.float64)
        #-------------------------------------#
        thinwalls_array = []
        #-------------------------------------#
        for twall in thin_walls:
            x,y = 0,0
            twall_array = [0 for _ in range(7)]
            #-------------------------------------#
            for key, value in twall.items():
                #-------------------------------------#
                match key:
                    #-------------------------------------#
                    case "x":
                        twall_array[0] = value
                    #-------------------------------------#
                    case "y":
                        twall_array[1] = value
                    #-------------------------------------#
                    case "direction":
                        twall_array[2] = value
                    #-------------------------------------#
                    case "length":
                        twall_array[3] = value
                    #-------------------------------------#
                    case "texture":
                        twall_array[4] = self.texture_handler.get_raytexture_id(value)
                    #-------------------------------------#
                    case "collision":
                        twall_array[5] = int(value)
                    #-------------------------------------#
                    case "eid":
                        if isinstance(value, str):
                            signal_bus.emit(signals.SPAWN_ENTITY, name=value, pos=[y,x])
                        twall_array[6] = -1
            thinwalls_array.append(twall_array)
        #-------------------------------------#
        return thinwalls_array
    #=====================================#
    def make_doors(self, doors:list[dict], thin_walls:list[dict]):
        #-------------------------------------#
        if doors is None:
            return np.empty((0, 11), dtype=np.float64)
        #-------------------------------------#
        doors_array = []
        #-------------------------------------#
        for dinfo in doors:
            doorinfo_array = [0 for _ in range(11)]
            #-------------------------------------#
            has_jamb = False
            jamb_texture = None
            texture = None
            x = 0
            closed_x = 0
            y = 0
            closed_y = 0
            direction = 0
            length = 1
            #-------------------------------------#
            for key, value in dinfo.items():
                #-------------------------------------#
                match key:
                    case "x":
                        x = value
                        doorinfo_array[0] = value
                    case "y":
                        y = value
                        doorinfo_array[1] = value
                    case "direction":
                        direction = value
                        doorinfo_array[2] = value
                    case "length":
                        length = value
                        doorinfo_array[3] = value
                    case "texture":
                        texture = value
                        doorinfo_array[4] = self.texture_handler.get_raytexture_id(value)
                    case "offset":
                        offset = value
                        doorinfo_array[5] = value
                    case "speed":
                        speed = value
                        doorinfo_array[6] = value
                    case "open_state":
                        if value == "closed":
                            value = 0
                        elif value == "closing":
                            value = 1
                        elif value == "open":
                            value = 2
                        elif value == "opening":
                            value = 3
                        elif value == "locked":
                            value = 4
                        elif value == "open_force":
                            value = 5
                        else:
                            value = 0
                        open_state = value
                        doorinfo_array[7] = value
                    case "has_jamb":
                        has_jamb = value
                        doorinfo_array[8] = int(value)
                        if value:
                            has_jamb = True
                    case "jamb_texture":
                        jamb_texture = value
                        doorinfo_array[9] = self.texture_handler.get_raytexture_id(value)
                    case "eid":
                        doorinfo_array[10] = -1
                #-------------------------------------#
            signal_bus.emit(signals.SPAWN_ENTITY, name=f"{assetsmarks.engine.entity}::raycaster3D.door", pos=[y,x], overrides={
                f"{assetsmarks.engine.components}::Door": {
                    "direction":direction,
                    "length":length,
                    "offset":offset,
                    "speed":speed,
                    "open_state":open_state,
                    "has_jamb":has_jamb
                }
            })
            #-------------------------------------#
            doors_array.append(doorinfo_array)
            #-------------------------------------#
            if has_jamb:
                jamb_texture = jamb_texture if jamb_texture is not None else texture
                twall_dir = not direction
                #-------------------------------------#
                if twall_dir:
                    twall_x = x
                    twall_x2 = x
                    twall_y = y + length/2 
                    twall_y2 = y - length/2 
                #-------------------------------------#
                else:
                    twall_x = x + length/2
                    twall_x2 = x - length/2
                    twall_y = y
                    twall_y2 = y
                #-------------------------------------#
                twall_array = [
                    twall_x, twall_y,
                    twall_dir,
                    length,
                    self.texture_handler.get_raytexture_id(jamb_texture),
                    0,
                    -1
                ]
                twall_array2 = [
                    twall_x2, twall_y2,
                    twall_dir,
                    length,
                    self.texture_handler.get_raytexture_id(jamb_texture),
                    0,
                    -1
                ]
                #-------------------------------------#
                thin_walls.append(twall_array)
                thin_walls.append(twall_array2)
        #-------------------------------------#
        return np.array(doors_array, dtype=np.float64), np.array(thin_walls, dtype=np.float64)
    #=====================================#
    def make_sprites(self, sprites:list[dict]):
        #-------------------------------------#
        if sprites is None:
            return np.empty((0, 6), dtype=np.float64)
        #-------------------------------------#
        sprites_array = []
        #-------------------------------------#
        for sprinfo in sprites:
            sprinfo_array = [0 for _ in range(6)]
            #-------------------------------------#
            for key, value in sprinfo.items():
                #-------------------------------------#
                match key:
                    #-------------------------------------#
                    case "x":
                        sprinfo_array[0] = value
                    #-------------------------------------#
                    case "y":
                        sprinfo_array[1] = value
                    #-------------------------------------#
                    case "texture":
                        sprinfo_array[2] = self.texture_handler.get_raytexture_id(value)
                    #-------------------------------------#
                    case "scale":
                        sprinfo_array[3] = value
                    #-------------------------------------#
                    case "offsetZ":
                        sprinfo_array[4] = value
                    #-------------------------------------#
                    case "eid":
                        if value == -1:
                            sprinfo_array[5] = -1
            sprites_array.append(sprinfo_array)
        #-------------------------------------#
        sprites_array = self.turn_entities_into_sprite(sprites_array)
        #-------------------------------------#
        return sprites_array

    def turn_entities_into_sprite(self, sprites_array:list[list]):
        #-------------------------------------#
        for entity, (pos, tex, scale, offsetZ, tag) in globalclasses.World.query(Position, Texture, Scale3D, OffsetZ3D, Sprite3DTag):
            #-------------------------------------#
            was_created = False
            #-------------------------------------#
            for sid, sprinfo in enumerate(sprites_array.copy()):
                if sprinfo[5] == entity:
                    was_created = True
                    break
            #-------------------------------------#
            if not was_created:
                #-------------------------------------#
                tex.texture = self.texture_handler.get_raytexture_id(tex.texture) if isinstance(tex.texture, str) else tex.texture
                #-------------------------------------#
                sprinfo = [
                    pos.x, pos.y,
                    tex.texture,
                    scale.scale,
                    offsetZ.offsetZ,
                    entity
                ]
                #-------------------------------------#
                sprites_array.append(sprinfo)
        #-------------------------------------#
        return sprites_array
        



