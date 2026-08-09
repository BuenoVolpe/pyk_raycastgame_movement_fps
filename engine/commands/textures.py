from engine.console import command, console
from engine.configs.configs import configs
from engine.signal_bus import signal_bus
#-----------------------#
from game.enums.signals import signals
#-----------------------#
@command("textures.log.atlas", protection_level=0)
def textures_log_show_atlas_keys():
    signal_bus.emit(signals.TEXTURE_LOG_ATLAS_DATA)
@command("textures.log.raytextures_ids", protection_level=0)
def textures_log_show_raytextures_ids():
    signal_bus.emit(signals.TEXTURE_LOG_RAYTEXTURES_ID)
    

