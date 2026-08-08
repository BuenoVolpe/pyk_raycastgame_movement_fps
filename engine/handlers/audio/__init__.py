import pygame as pg
#--------------------------------#
from engine.signal_bus import signal_bus
from game.enums.signals import signals
from game.enums.signals_prioritys import signals_prioritys
from game.enums.assets_marks import assetsmarks
#--------------------------------#
from engine.configs.configs import configs
#--------------------------------#
#--------------------------------#
from engine.utils.debug_log import debug_log
from engine.utils.log import log, log_list, log_dict
from engine.utils.dict_to_class import dict_to_class
#================================#
from engine.handlers.audio.atlas import Atlas
from engine.handlers.audio.loader import Loader
from engine.handlers.audio.player import Player
#================================#
class AudioHandler:
    #--------------------------------#
    def __init__(self):
        #--------------------------------#
        self.paths = dict_to_class({
            "error": configs.paths.audio_error,
            configs.engine.acronym: configs.paths.engine.audio,
            configs.game.acronym: configs.paths.game.audio,
        })
        #--------------------------------#
        self.atlas = Atlas(self.paths.error)
        self.player = Player(self.paths, self.atlas)
        self.loader = Loader(self.paths, self.atlas)
        self.loader._load()
        #================================#
        signal_bus.subscribe(signals.SOUND_PLAY, self.play, priority=signals_prioritys.SOUND)
        signal_bus.subscribe(signals.SOUND_PLAY_GROUP, self.play_group, priority=signals_prioritys.SOUND)
        #================================#
        signal_bus.subscribe(signals.AUDIO_LOG_ATLAS_DATA, lambda: log_list(list(self.atlas.data.keys()), list_name="sound atlas data",console=True), priority=signals_prioritys.SOUND)
        signal_bus.subscribe(signals.AUDIO_LOG_GROUPS_DATA, lambda: log_dict(self.atlas.groups_data, dict_name="sound atlas groups data",console=True), priority=signals_prioritys.SOUND)
        signal_bus.subscribe(signals.AUDIO_LOG_MUSIC_DATA, lambda: log_list(list(self.atlas.music_data.keys()), list_name="sound atlas music data",console=True), priority=signals_prioritys.SOUND)
        #================================#
        debug_log(f"{assetsmarks.engine.debug}::audio.show_atlas_keys", 
                  value=list(self.atlas.data.keys())
                  )
        debug_log(f"{assetsmarks.engine.debug}::audio.show_groups_dict", 
                  value=self.atlas.groups_data)
        debug_log(f"{assetsmarks.engine.debug}::audio.show_music_atlas_keys", 
                  value=list(self.atlas.music_data.keys())
                  )
    #================================#
    def play(self, sound:str, **kwargs):    
        #--------------------------------#
        self.player.play(sound, **kwargs)
    #================================#
    def play_group(self, sound:str, **kwargs):    
        #--------------------------------#
        self.player.play_group(sound, **kwargs)
