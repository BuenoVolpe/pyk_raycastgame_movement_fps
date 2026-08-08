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
class EntityFactory:
    def __init__(self, world):
        #-------------------------------------#
        self.paths = {
            configs.engine.acronym: configs.paths.engine.entities,
            configs.game.acronym: configs.paths.game.entities,
        }
        #-------------------------------------#
        self.entity_registry = {}
        self.load_registry()
        #-------------------------------------#
        debug_log(f"{assetsmarks.engine.debug}::ecs.entities_keys", 
                value=list(self.entity_registry.keys())
                )
        #-------------------------------------#
        self.world = world
        #-------------------------------------#
        self.component_map = COMPONENT_REGISTRY
        #--------------------------------z-----#
        signal_bus.subscribe(signals.SPAWN_ENTITY, self.spawn_entity, priority=signals_prioritys.ADD_OBJ)
        signal_bus.subscribe(signals.CREATE_ENTITY_BY_DATA, self.build_entity_from_data, priority=signals_prioritys.ADD_OBJ)
        signal_bus.subscribe(signals.APPLY_OVERRIDES, self.apply_overrides, priority=signals_prioritys.ADD_OBJ)
        #--------------------------------z-----#
        # self.entity_templates = {}
        # self.load_entity_templates()
    #=====================================#
    def load_registry(self):
        for origin, path in self.paths.items():
            #-------------------------------------#
            for info in scan_folder_for_json(path):
                json_path = info["json_path"]
                #-------------------------------------#
                relative = os.path.relpath(json_path, path)
                #-------------------------------------#
                entity_id = (
                    relative
                    .replace(".json", "")
                    .replace("\\", ".")
                    .replace("/", ".")
                )
                #-------------------------------------#
                if origin == configs.engine.acronym:
                    entity_id = f"{assetsmarks.engine.entity}::{entity_id}"
                else:
                    entity_id = f"{assetsmarks.engine.game}::{entity_id}"
                #-------------------------------------#
                self.entity_registry[entity_id] = json_path    
    #=====================================#
    def create_entity(self, entity_name:str):
        json_path = self.entity_registry.get(entity_name)
        #-------------------------------------#
        json_data = json_reader(json_path)
        json_data["entity_name"] = entity_name if not json_data.get("type") else json_data.get("type")
        #-------------------------------------#
        return self.build_entity_from_data(json_data)
    #=====================================#
    def resolve_extends(self, data):
        #-------------------------------------#
        parent_name = data.get("extends")
        #-------------------------------------#
        if not parent_name:
            return data
        #-------------------------------------#
        parent_path = self.entity_registry.get(parent_name)
        #-------------------------------------#
        if not parent_path:
            #-------------------------------------#
            log_error(f"Parent entity {parent_name} not found")#, console)
            return data
        #-------------------------------------#
        parent_data = json_reader(parent_path)
        #-------------------------------------#
        parent_data = self.resolve_extends(parent_data)
        #-------------------------------------#
        merged = deep_merge(parent_data, data)
        #-------------------------------------#
        merged.pop("extends", None)
        #-------------------------------------#
        return merged
    #=====================================#
    def build_entity_from_data(self, data, do_log_errors:bool=True, do_log_id:bool=False):
        #-------------------------------------#
        entity = self.world.create_entity()
        #-------------------------------------#
        data = self.resolve_extends(data)
        #-------------------------------------#
        entity_type = data.get("entity_name") or data.get("type")
        #-------------------------------------#
        if entity_type:
            self.world.add_component(
                entity,
                EntityType(entity_type)
            )
        #-------------------------------------#
        components = copy.deepcopy(data.get("components", {}))
        extends = copy.deepcopy(data.get("extends"))
        #-------------------------------------#
        errors = 0
        #-------------------------------------#
        for comp_name, comp_values in components.items():
            #-------------------------------------#
            comp_class = self.component_map.get(comp_name)
            #-------------------------------------#
            if comp_class:
                #-------------------------------------#
                if isinstance(comp_values, dict):
                    #-------------------------------------#
                    for key, value in comp_values.items():
                        #-------------------------------------#
                        if isinstance(value, dict):
                            #-------------------------------------#
                            if "choice" in value:
                                #-------------------------------------#
                                comp_values[key] = random.choice(value["choice"])
                            #-------------------------------------#
                            elif "random" in value:
                                #-------------------------------------#
                                comp_values[key] = random.randint(*value["random"])
                            #-------------------------------------#
                            elif "random_float" in value:
                                #-------------------------------------#
                                comp_values[key] = random.uniform(*value["random_float"])
                #-------------------------------------#
                if validate_component(comp_class, comp_values):
                    #-------------------------------------#
                    component = comp_class(**comp_values)
                    self.world.add_component(entity, component)
                #-------------------------------------#    
                continue
                #-------------------------------------#    
            else:
                errors += 1
                log_error(f"[ent_factory]: can't find Component: {comp_name}")
        #-------------------------------------#
        if do_log_errors and errors:
            log_error(f"[ent_factory]: find {errors} errors, while creating entity", True)
        #-------------------------------------#
        if do_log_id:
            log_success(f"entity:{entity} was created with data:{data}", True)
        #-------------------------------------#
        return entity
    #=====================================#
    def spawn_entity(self, name: str, pos:list[float, float]=None, overrides:dict={}):
        overrides = overrides or {}
        #-------------------------------------#
        if pos:
            overrides[f"{assetsmarks.engine.components}::Position"] = {"x":pos[0], "y":pos[1]}
        #-------------------------------------#
        entity = self.create_entity(name)
        #-------------------------------------#
        if overrides:
            self.apply_overrides(entity, overrides)
        #-------------------------------------#
        return entity
    #=====================================#
    def apply_overrides(self, entity, overrides: dict):
        """
        overrides format:
        {
            "component@pyk::Transform": {"x": 10, "y": 20},
            "component@pyk::Health": {"value": 999}
        }
        """
        #-------------------------------------#
        for comp_name, values in overrides.items():
            #-------------------------------------#
            comp_class = self.component_map.get(comp_name)
            #-------------------------------------#
            if not comp_class:
                log_error(f"Override component not found: {comp_name}")#, console)
                continue
            #-------------------------------------#
            storage = self.world.get_storage(comp_class)
            component = storage.get(entity) if storage else None
            #-------------------------------------#
            if component:
                #-------------------------------------#
                if isinstance(values, list):
                    log_error("list are not acepted")#, console) 
                for k, v in values.items():
                    setattr(component, k, v)
            #-------------------------------------#
            else:
                #-------------------------------------#
                component = comp_class(**values)
                print(component, comp_name,entity)
                self.world.add_component(entity, component)

#=====================================#
def validate_component(comp_class, data):
    #-------------------------------------#
    try:
        #-------------------------------------#
        comp_class(**data)
    #-------------------------------------#
    except Exception as e:
        #-------------------------------------#
        log_error(f"[ent_factory]: Error at Component {comp_class.__name__}: {e}")
        return False
    #-------------------------------------#
    return True
#=====================================#
def deep_merge(base: dict, override: dict):
    #-------------------------------------#
    result = copy.deepcopy(base)
    #-------------------------------------#
    for key, value in override.items():
        #-------------------------------------#
        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(value, dict)
        ):
        #-------------------------------------#
            result[key] = deep_merge(result[key], value)
        #-------------------------------------#
        else:
            result[key] = copy.deepcopy(value)
        #-------------------------------------#
    return result
        


