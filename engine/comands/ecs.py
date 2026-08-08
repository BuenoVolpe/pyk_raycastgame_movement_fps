from engine.console import command, console
from engine.configs.configs import configs
#-----------------------#
from engine.signal_bus import signal_bus
from game.enums.signals import signals
from game.enums.signals_prioritys import sig_prio
#-----------------------#
@command("load_world", protection_level=1)
def load_world(name:str):
    """load a word with a centarn name"""
    signal_bus.emit(signals.LOAD_WORLD, world_id=name)
    #-----------------------#
    return f"trying to load world: {name}..." 
#-----------------------#
@command("spawn", protection_level=1)
def spawn(name:str, pos:list[float, float]=None, overrides:dict={}):
    #-----------------------#
    console.log(name, "white")
    signal_bus.emit(signals.LOAD_WORLD, name=name, pos=pos, overrides=overrides)
    #-----------------------#
    return f"trying to load world: {name}..."
#-----------------------#
@command("ecs.entity.apply_overrides", protection_level=1)
def apply_overrides(entity:int, overrides:dict):
    #-----------------------#
    signal_bus.emit(signals.APPLY_OVERRIDES, entity=entity, overrides=overrides)
    return f"overrides: {overrides} apllied for: {overrides}"
#-----------------------#
@command("ecs.entity.create", protection_level=2)
def create_entity():
    signal_bus.emit(signals.CREATE_ENTITY, log_id=True)
#-----------------------#
@command("ecs.entity.kill", protection_level=2)
def kill_entity(entity):
    signal_bus.emit(signals.KILL_ENTITY, entity=entity)
    return f"entity: {entity} was killed"
#-----------------------#
@command("ecs.entity.create.from_data", protection_level=2)
def build_entity_from_data(data:dict, do_log_errors:bool=False):
    signal_bus.emit(signals.CREATE_ENTITY_BY_DATA, data=data, do_log_errors=do_log_errors, do_log_id=True)
#-----------------------#
@command("ecs.component.add", protection_level=2)
def add_component(entity, component):
    signal_bus.emit(signals.ADD_COMPONENT, entity=entity, component=component)
#-----------------------#
@command("ecs.component.remove", protection_level=2)
def remove_component(entity, comp_type):
    signal_bus.emit(signals.REMOVE_COMPONENT, entity=entity, comp_type=comp_type)

