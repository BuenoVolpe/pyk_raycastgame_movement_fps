import random
import os
import copy
#=====================================#
from engine.utils.json import json_reader, scan_folder_for_json
from engine.utils.debug_log import debug_log
from engine.utils.overlay import debug_overlay
from engine.utils.log import log_error, log_success
from engine.utils.dict_to_class import dict_to_class
#-------------------------------------#
from engine.configs.configs import configs
#-------------------------------------#
from engine.signal_bus import signal_bus
from game.enums.signals import signals
from game.enums.signals_prioritys import signals_prioritys
from game.enums.assets_marks import assetsmarks
#-------------------------------------#
from engine.ecs.component_storage import COMPONENT_REGISTRY
from engine.ecs.components.all import *
from engine.ecs.systems.all import *
#=====================================#
class WorldFactory:
    def __init__(self, world, entity_factory):
        #-------------------------------------#
        self.paths = {
            configs.engine.acronym: configs.paths.engine.worlds,
            configs.game.acronym: configs.paths.game.worlds,
        }
        #------------------------+-------------#
        self.world_registry = {}
        self._load_registry()
        #-------------------------------------#
        debug_log(f"{assetsmarks.engine.debug}::ecs.world_keys", 
                value=list(self.world_registry.keys())
                )
        debug_overlay.watch(
            f"{assetsmarks.engine.debug}::overlay.world_name",
            lambda: f"{self.world_name}"
        )
        #-------------------------------------#
        self.entity_factory = entity_factory
        self.world = world
        #-------------------------------------#
        signal_bus.subscribe(signals.LOAD_WORLD, self.load_world, priority=signals_prioritys.LOAD)
        #-------------------------------------#
    #=====================================#
    def load_world(self, world_id:str):
        #-------------------------------------#
        world_path = self.world_registry.get(world_id)
        if world_path is None:
            log_error(f"world {world_id} not found", True)
            return
        #-------------------------------------#
        self.world.clear()
        self.world_name = world_id
        world_data = json_reader(world_path)
        #-------------------------------------#
        entities = world_data.get("entities", [])
        if entities:
            #-------------------------------------#
            for i, entity_data in enumerate(entities):
                #-------------------------------------#
                prefab = entity_data.get("prefab")
                positions = entity_data.get("positions")
                overrides = entity_data.get("overrides")
                #-------------------------------------#
                if not prefab:
                    log_error(f"entity of index {i} has no prefab")
                    continue
                if not self.entity_factory.entity_registry.get(prefab):
                    log_error(f"entity {prefab} does not exist")
                    continue
                #-------------------------------------#
                if not positions:
                    signal_bus.emit(signals.SPAWN_ENTITY, name=prefab, overrides=overrides)
                    debug_log(f"{assetsmarks.engine.debug}::ecs.entities_loaded_in_world", 
                            value=f"[world_factory]: spawned entity {prefab} with index {i}"
                            )
                    continue
                #-------------------------------------#
                for num, pos in enumerate(positions):
                    signal_bus.emit(signals.SPAWN_ENTITY, name=prefab, pos=pos, overrides=overrides)
                #-------------------------------------#
                debug_log(f"{assetsmarks.engine.debug}::ecs.entities_loaded_in_world", 
                        value=f"[world_factory]: spawned {num+1} entities {prefab} with index {i}"
                        )
                #-------------------------------------#
            #-------------------------------------#
            signal_bus.emit(signals.LOAD_COMPLETE_WORLD, name=world_id, data=world_data)
            log_success(f"world {world_id} loaded with {len(entities)} entities", True)
        #-------------------------------------#
        else:
            log_error(f"world {world_id} has no entities", True)
    #=====================================#
    def _load_registry(self):
        for origin, path in self.paths.items():
            #-------------------------------------#
            for info in scan_folder_for_json(path):
                json_path = info["json_path"]
                #-------------------------------------#
                relative = os.path.relpath(json_path, path)
                #-------------------------------------#
                world_id = (
                    relative
                    .replace(".json", "")
                    .replace("\\", ".")
                    .replace("/", ".")
                )
                #-------------------------------------#
                world_id = f"{assetsmarks.engine.world}::{world_id}"
                #-------------------------------------#
                self.world_registry[world_id] = json_path
