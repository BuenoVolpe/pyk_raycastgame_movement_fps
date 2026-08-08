#================================#
import pygame as pg
from random import choice
#================================#
from engine.configs.configs import configs
#================================#
from engine.utils.log import log_error
from engine.utils.dict_to_class import dict_to_class
#================================#
class Atlas:
    def __init__(self, error_audio):
        self.error_audio_path = error_audio
        #--------------------------------#
        self.data = {}
        self.groups_data = {} #string: [string_a, string_b]
        self.music_data = {}
        #--------------------------------#
        self.error_already_happen = False
        self.error_audio = dict_to_class({
            "sound": pg.mixer.Sound(error_audio),
            "category": "sfx"
            })
        #--------------------------------#
        self.save(f"{configs.engine.asset_marks.audio}@{configs.engine.acronym}::error", self.error_audio)

    #================================#
    def save_in_group(self, group:str, name:str):
        #--------------------------------#
        if group not in self.groups_data:
            self.groups_data[group] = []
        #--------------------------------#
        self.groups_data[group].append(name)

    #================================#
    def save_as_music(self, name:str, music):
        #--------------------------------#
        self.music_data[name] = music

    #================================#
    def save(self, name:str, audio):
        #--------------------------------#
        self.data[name] = audio

    #================================#
    def get_from_group(self, group:str, return_string_mode=False):
        #--------------------------------#
        list = self.groups_data.get(group)
        #--------------------------------#
        if not list:
            log_error(f"Group '{group}' not found in atlas. Returning error sound.", True)
            return self.error_audio
        #--------------------------------#
        name = choice(list)
        audio = self.data.get(name)
        #--------------------------------#
        if not audio:
            log_error(f"can't find sound {name} in group {group}, returning error sound")
            #--------------------------------#
            if return_string_mode:
                return self.error_audio_path
            return self.error_audio
        #--------------------------------#
        if return_string_mode:
            return name
        return audio
        
    def get(self, name:str):
        #--------------------------------#
        audio = self.data.get(name)
        #--------------------------------#
        if not audio:
            log_error(f"Sound '{name}' not found in atlas. Returning error sound.", True)
            return self.error_audio
        #--------------------------------#
        return audio
    #================================#
    def random(self):
        """
        Returns a random sprite from the atlas (debug purpose).
        """
        return choice(list(self.data.values()))

