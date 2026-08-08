from engine.configs.configs import configs
#--------------------------------#
from game.enums.signals import signals
from game.enums.signals_prioritys import signals_prioritys
from game.enums.assets_marks import assetsmarks
#--------------------------------#
from engine.signal_bus import signal_bus
#--------------------------------#
from engine.ecs.component_storage import ComponentStorage, COMPONENT_REGISTRY 
from engine.ecs.components.all import EntityType, PlayerTag
#--------------------------------#
from game.ecs.hooks import HOOK_REGISTRY 
#--------------------------------#
from engine.utils.overlay import debug_overlay
from engine.utils.debug_log import debug_log
from engine.utils.log import log, log_error, log_list, log_success
#================================#
class World:
    #--------------------------------#
    def __init__(self, game):
        self.game = game
        #--------------------------------------#
        self.next_entity = 0
        self.entities_amount = 0
        #--------------------------------------#
        self.components = {}
        self.query_cache = {}
        self.sprite_to_entity = {}
        #--------------------------------------#
        self.hooks = HOOK_REGISTRY
        #--------------------------------------#
        self.to_remove = set()
        #--------------------------------------#
        signal_bus.subscribe(signals.KILL_ENTITY, self.remove_entity, priority=signals_prioritys.ADD_OBJ)
        signal_bus.subscribe(signals.CREATE_ENTITY, self.create_entity, priority=signals_prioritys.REMOVE_OBJ)
        signal_bus.subscribe(signals.ADD_COMPONENT, self.add_component, priority=signals_prioritys.AFTER_REMOVE_OBJ)
        signal_bus.subscribe(signals.REMOVE_COMPONENT, self.remove_component, priority=signals_prioritys.AFTER_REMOVE_OBJ)
        #================================#
        debug_overlay.watch(
            f"{assetsmarks.engine.debug}::overlay.entities_amount",
            lambda: self.entities_amount
        )
        debug_log(
            f"{assetsmarks.engine.debug}::ecs.components_keys", value=list(COMPONENT_REGISTRY.keys())
        )
    #================================#
    def get_component(self, entity:int, comp_type:object):
        #--------------------------------------#
        storage = self.get_storage(comp_type)
        return storage.get(entity)
    #================================#
    def create_entity(self, log_id=False):
        #--------------------------------------#
        eid = self.next_entity
        self.next_entity += 1
        self.entities_amount += 1
        #--------------------------------------#
        debug_log(f"{assetsmarks.engine.debug}::ecs.create_entity", 
                value=f"[ecs_world]: created entity with id: {eid}"
                )
        #--------------------------------------#
        if log_id:
            log_success(f"created entity with id:{eid}", True)
        #--------------------------------------#
        return eid
    #================================#
    def clear(self):
        #--------------------------------------#
        for storage in self.components.values():
            storage.data.clear()
        #--------------------------------------#
        self.components.clear()
        self.query_cache.clear()
        self.sprite_to_entity.clear()
        self.to_remove.clear()
        #--------------------------------------#
        self.next_entity = 0 
        self.entities_amount = 0
        #--------------------------------------#
        debug_log(f"{assetsmarks.engine.debug}::ecs.clear", 
                value="[ecs_world]: cleared"
                )
    #================================#
    def remove_entity(self, entity:int):
        #--------------------------------------#
        self.to_remove.add(entity)
        #--------------------------------------#
        self.query_cache.clear()
        #--------------------------------------#
    #================================#
    def flush(self):
        #--------------------------------------#
        for entity in self.to_remove:
            #--------------------------------------#
            self.entities_amount -= 1
            #--------------------------------------#
            for storage in self.components.values():
            #--------------------------------------#
                storage.data.pop(entity, None)
            #--------------------------------------#
            debug_log(f"{assetsmarks.engine.debug}::ecs.remove_component", 
                    value=f"[ecs_world]: removed entity with id {entity}"
                    )
        #--------------------------------------#
        self.to_remove.clear()
    #================================#
    def remove_component(self, entity:int, comp_type:object|str):
        if isinstance(comp_type, str):
            if comp_type := COMPONENT_REGISTRY.get(comp_type) is None:
                log_error(f"[ecs_world]: component:{comp_type} is not a valid component")
                return
        #--------------------------------------#
        storage = self.get_storage(comp_type)
        storage.remove(entity)
        #--------------------------------------#
        debug_log(f"{assetsmarks.engine.debug}::ecs.remove_component", 
                value=f"[ecs_world]: removed component {comp_type} from entity:{entity}"
                )
        #--------------------------------------#
        self.query_cache.clear()
    #================================#
    def get_entity_components(self, entity:int):
        #--------------------------------------#
        comps = {}
        #--------------------------------------#
        for comp_type, storage in self.components.items():
            #--------------------------------------#
            comp = storage.get(entity)
            if comp is not None:
                comps[comp_type.__name__] = comp
            #--------------------------------------#
        return comps
    #================================#
    def get_player(self):
        for entity, tag in self.query(PlayerTag):
            comp = self.get_entity_components(entity)
            return entity, comp
    #================================#
    def get_storage(self, comp_type:object):
        #--------------------------------------#
        if comp_type not in self.components:
            #--------------------------------------#
            self.components[comp_type] = ComponentStorage()
        #--------------------------------------#
        return self.components[comp_type]
    #================================#
    def add_component(self, entity:int, component:object|str):
        if isinstance(component, str):
            if component := COMPONENT_REGISTRY.get(component) is None:
                log_error(f"[ecs_world]: component:{component} is not a valid component")
                return
        #--------------------------------------#
        comp_type = type(component)
        #--------------------------------------#
        storage = self.get_storage(comp_type)
        storage.add(entity, component)
        #--------------------------------------#
        if comp_type in self.hooks:
            hook = self.hooks[comp_type]
            hook(entity, component, self.game)
        #--------------------------------------#
        debug_log(f"{assetsmarks.engine.debug}::ecs.add_component", 
                value=f"[ecs_world]: added component {component} to entity:{entity}"
                )
        #--------------------------------------#
        self.query_cache.clear()
    #================================#
    def query(self, *include:object, exclude:tuple[object]=()):
        #--------------------------------------#
        key = (include, exclude)
        #--------------------------------------#
        if key in self.query_cache:
            #--------------------------------------#
            base, include_storages, exclude_storages = self.query_cache[key]
        #--------------------------------------#
        else:
            #--------------------------------------#
            include_storages = [self.get_storage(c) for c in include]
            exclude_storages = [self.get_storage(c) for c in exclude]
            #--------------------------------------#
            if not include_storages:
                return
            #--------------------------------------#
            base = min(include_storages, key=lambda s: len(s.data))
            #--------------------------------------#
            self.query_cache[key] = (base, include_storages, exclude_storages)
        #--------------------------------------#
        for entity in base.data:
            #--------------------------------------#
            components = []
            #--------------------------------------#
            for storage in include_storages:
                #--------------------------------------#
                comp = storage.get(entity)
                #--------------------------------------#
                if comp is None:
                    break
                #--------------------------------------#
                components.append(comp)
            #--------------------------------------#
            else:
                #--------------------------------------#
                for storage in exclude_storages:
                    #--------------------------------------#
                    if storage.has(entity):
                        #--------------------------------------#
                        break
                #--------------------------------------#
                else:
                    yield entity, tuple(components)
    #================================#
    def get_entities_with_type(self, *types):
        storage = self.get_storage(EntityType)
        for entity, component in storage.data.items():
            if component.name in types:
                yield entity, component

