from game.enums.assets_marks import assetsmarks
from engine.utils.debug_log import debug_log
#================================#
COMPONENT_REGISTRY = {}
#--------------------------------#
def register_game_component(cls):
    #--------------------------------#
    COMPONENT_REGISTRY[f"{assetsmarks.game.components}::{cls.__name__}"] = cls
    return cls
def register_engine_component(cls):
    #--------------------------------#
    COMPONENT_REGISTRY[f"{assetsmarks.engine.components}::{cls.__name__}"] = cls
    return cls
#================================#
class ComponentStorage:
    #--------------------------------#
    def __init__(self):
        self.data = {}  # entity_id -> component
    #--------------------------------#
    def add(self, entity:int, component:object):
        self.data[entity] = component
    #--------------------------------#
    def get(self, entity:int):
        return self.data.get(entity)
    #--------------------------------#
    def remove(self, entity:int):
        #--------------------------------#
        if entity in self.data:
            del self.data[entity]
    #--------------------------------#
    def has(self, entity:int):
        #--------------------------------#
        return entity in self.data
