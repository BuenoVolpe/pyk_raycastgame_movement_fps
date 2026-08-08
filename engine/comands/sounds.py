from engine.console import command, console
from engine.configs.configs import configs
from engine.signal_bus import signal_bus
from game.enums.signals import signals
#-----------------------#
@command("sounds.log.atlas_data")
def AUDIO_LOG_ATLAS_DATA():
    signal_bus.emit(signals.AUDIO_LOG_ATLAS_DATA)
#-----------------------#
@command("sounds.log.groups_data")
def AUDIO_LOG_GROUPS_DATA():
    signal_bus.emit(signals.AUDIO_LOG_GROUPS_DATA)
#-----------------------#
@command("sounds.log.music_data")
def AUDIO_LOG_MUSIC_DATA():
    signal_bus.emit(signals.AUDIO_LOG_MUSIC_DATA)
#-----------------------#
@command("sounds.play")
def SOUND_PLAY(        name: str,
        source_pos: tuple | None = None,
        listener_pos: tuple | None = None,
        listener_forward: tuple | None = None,
        max_distance: float | None = None,
        min_distance: float | None = None,):
    signal_bus.emit(signals.SOUND_PLAY, 
                    name=name, source_pos=source_pos, listener_pos=listener_pos, 
                    listener_forward=listener_forward, max_distance=max_distance, min_distance=min_distance)
#-----------------------#
@command("sounds.play3d")
def SOUND_PLAY_GROUP(group:str, source_pos:tuple|None=None, listener_pos:tuple|None=None, max_distance:float=None,min_distance:float=None):
    signal_bus.emit(signals.SOUND_PLAY_GROUP, group=group,source_pos=source_pos,listener_pos=listener_pos,max_distance=max_distance,min_distance=min_distance)
#-----------------------#