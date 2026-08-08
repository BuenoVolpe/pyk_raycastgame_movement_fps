import os
import pygame as pg
#--------------------------------#
from engine.signal_bus import signal_bus
from game.enums.signals import signals
from game.enums.signals_prioritys import signals_prioritys
from game.enums.assets_marks import assetsmarks
#--------------------------------#
from engine.configs.configs import configs
#--------------------------------#
from engine.utils.log import log, log_error
from engine.utils.json import scan_folder
from engine.utils.dict_to_class import dict_to_class
#================================#
from engine.handlers.audio.atlas import Atlas
#================================#
class Loader:
    def __init__(self, paths:object, atlas:object):
        #-------------------------------------#
        self.engine_path = getattr(paths, configs.engine.acronym)
        self.game_path = getattr(paths, configs.game.acronym)
        #-------------------------------------#
        self.paths = {
            configs.engine.acronym: self.engine_path,
            configs.game.acronym: self.game_path
        }
        #-------------------------------------#
        self.atlas = atlas
        #-------------------------------------#
        # self._load()
    #=====================================#
    def _load(self):
        #-------------------------------------#
        engine_asset = assetsmarks.engine.audio
        engine_music_asset = assetsmarks.engine.music
        engine_group = assetsmarks.engine.audiogroup
        #-------------------------------------#
        game_asset = assetsmarks.game.audio
        game_music_asset = assetsmarks.game.music
        game_group = assetsmarks.game.audiogroup
        #=====================================#
        for base, path in self.paths.items():
            for (full_path, name) in scan_folder(path, extension=f".{configs.engine.extensions.audio}"):
                #-------------------------------------#
                rel = os.path.relpath(full_path, path)
                #--------------------------------#
                parts = rel.split(os.sep)
                #--------------------------------#
                category = parts[0] if len(parts) > 1 else "sfx"
                group = parts[1] if len(parts) > 2 else category
                #--------------------------------#
                key = rel.replace(f".{configs.engine.extensions.audio}", "").replace("\\", ".")
                #--------------------------------#
                data = dict_to_class({
                    "sound": pg.mixer.Sound(full_path),
                    "category": category
                })
                #-------------------------------------#
                if base == configs.engine.acronym:
                    atlas_path = f"{engine_asset}::{key}"
                    #--------------------------------#
                    if category == configs.engine.music_folder:
                        data.sound = full_path
                        music_atlas_path = f"{engine_music_asset}::{key.replace(f"{configs.engine.music_folder}.", "", 1)}"
                        self.atlas.save_as_music(music_atlas_path, data)
                    #--------------------------------#
                    elif category != group:
                        group_atlas_path = f"{engine_group}::{group}"
                        self.atlas.save_in_group(group_atlas_path, atlas_path)
                    #--------------------------------#
                elif base == configs.game.acronym:
                    #--------------------------------#
                    atlas_path = f"{game_asset}::{key}"
                    #--------------------------------#
                    if category == configs.engine.music_folder:
                        data.sound = full_path
                        music_atlas_path = f"{game_music_asset}::{key.replace(f"{configs.engine.music_folder}.", "", 1)}"
                        self.atlas.save_as_music(music_atlas_path, data)
                    #--------------------------------#
                    elif category != group:
                        group_atlas_path = f"{game_group}::{group}"
                        self.atlas.save_in_group(group_atlas_path, atlas_path)
                #--------------------------------#
                self.atlas.save(atlas_path, data)
