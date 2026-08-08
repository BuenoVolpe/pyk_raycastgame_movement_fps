import pygame as pg
import time
from sys import exit
#=====================================#
from game.main.display import Display
from game.main.events_handler import EventsHandler
from game.main.loader import Loader
from game.main.updater import Updater
from game.main.render import Render
#=====================================#
from engine.raycaster3D.constants import worldMap
#=====================================#
from engine.comands.all import *
from engine.console import console
#=====================================#
from engine.utils.debug_log import debug_log
from engine.utils.overlay import debug_overlay
from engine.utils.globalclasses import globalclasses
from engine.handlers.textures import TextureHandler
#=====================================#
from engine.ecs import World
from engine.ecs.entity_factory import EntityFactory
from engine.ecs.world_factory import WorldFactory
from engine.ecs.components.all import Position, Texture
from game.world_loader import WorldLoader
#=====================================#
from engine.handlers.audio import AudioHandler
from engine.handlers.fonts import fonts
#=====================================#
from engine.configs.configs import configs
#-------------------------------------#
from engine.camera import Camera
#-------------------------------------#
from engine.signal_bus import signal_bus
from game.enums.signals import signals
from game.enums.signals_prioritys import sig_prio
from game.enums.assets_marks import assetsmarks
#=====================================#
pg.init()
pg.key.set_repeat(400, 40)
pg.mixer.init()
#=====================================#
class Main:
    #=====================================#
    def __init__(self):
        #-------------------------------------#
        self._load()
    #=====================================#
    def _load(self):
        #-------------------------------------#
        self.clock = pg.time.Clock()
        #=====================================#
        self.prev_time = 0
        #=====================================#
        self.world = World(self)
        self.entity_factory = EntityFactory(self.world)
        self.world_loader = WorldLoader()
        self.world_factory = WorldFactory(self.world, self.entity_factory)
        #=====================================#
        self.camera = Camera()
        globalclasses.Camera = self.camera
        #=====================================#
        self.display:Display = Display()
        self.loader:Loader = Loader()
        self.updater:Updater = Updater(self.world, worldMap)
        self.render:Render = Render(self.world)
        self.events_handler:EventsHandler = EventsHandler(self.world)
        #=====================================#
        self.texture_handler = TextureHandler()
        self.audio_handler = AudioHandler()
        #=====================================#
        pg.display.set_icon(self.texture_handler.get(configs.game.icon))
        #=====================================#
        # signal_bus.emit(signals.RENDER_ADD_IMG, image=self.texture_handler.get(f"{configs.engine.asset_marks.texture}@pyk::dave.standart"), pos=[5,5])
        # signal_bus.emit(signals.SOUND_PLAY_GROUP, sound=f"audiogroup@pyk::cats")
        # signal_bus.emit(signals.SOUND_PLAY, sound=f"{configs.engine.asset_marks.audio}@pyk::error")
        #=====================================#
        self.screen = self.display.screen
        self.main_surface = self.display.main_surface
        #=====================================#
        self.running = True
        self.time = 0
        self.dt = 0
        #=====================================#
        globalclasses.TextureHandler = self.texture_handler
        globalclasses.EntityFactory = self.entity_factory
        globalclasses.WorldFactory = self.world_factory
        globalclasses.World = self.world
        globalclasses.AudioHandler = self.audio_handler
        globalclasses.fonts = fonts
        globalclasses.signal_bus = signal_bus
        globalclasses.engine = self
        #=====================================#
        self.world_factory.load_world(f"{assetsmarks.engine.world}::raycaster3D.test")
        # self.entity_factory.create_entity(f"{assetsmarks.engine.entity}::raycaster3D.camera")
        # self.entity_factory.create_entity(f"{assetsmarks.engine.entity}::image_random")
        # self.entity_factory.create_entity(f"{assetsmarks.engine.entity}::image_move")
        # self.entity_factory.spawn_entity(f"{assetsmarks.engine.entity}::image_move", [0, 40], 
        #                                  {f"{assetsmarks.engine.components}::Texture": {"texture":f"{assetsmarks.engine.texture}::kaizer"}})
        # enty = self.world.create_entity()
        # self.world.add_component(enty, Texture(f"{assetsmarks.engine.texture}::dave.standart"))
        # self.world.add_component(enty, Position(0, 0))
        #=====================================#
        debug_overlay.watch(
            f"{assetsmarks.engine.debug}::overlay.engine_version",
            lambda: f"{configs.engine.version}"
        )
        debug_overlay.watch(
            f"{assetsmarks.engine.debug}::overlay.game_version",
            lambda: f"{configs.game.version}::{configs.engine.acronym}-{configs.engine.version}"
        )
        debug_overlay.watch(
            f"{assetsmarks.engine.debug}::overlay.fps",
            lambda: f"{self.clock.get_fps():.1f}"
        )
        debug_overlay.watch(
            f"{assetsmarks.engine.debug}::overlay.delta_time",
            lambda: f"{self.dt*(10**3):.1f}/1000"
        )
        debug_overlay.watch(
            f"{assetsmarks.engine.debug}::overlay.game_time",
            lambda: self.show_time(concatenate=True)
        )
        debug_overlay.watch(
            f"{assetsmarks.engine.debug}::overlay.game_ms",
            lambda: int(self.show_time(concatenate=False))
        )
        debug_overlay.watch(
            f"{assetsmarks.engine.debug}::overlay.player_pos",
            lambda: (
                f"{self.world.get_player()[1].get("Position").x:.1f}, y:{self.world.get_player()[1].get("Position").y:.1f}"
                if self.world.get_player()[1].get("Position") else None
                )
        )
        debug_overlay.watch(
            f"{assetsmarks.engine.debug}::overlay.player_angle",
            lambda: (
                f"{self.world.get_player()[1].get("Angle").angle:.1f}"
                if self.world.get_player()[1].get("Angle") else None
                )
        )
        debug_overlay.watch(
            f"{assetsmarks.engine.debug}::overlay.player_plane",
            lambda: (
                f"x:{self.world.get_player()[1].get("Camera3D").plane.x:.1f}, {self.world.get_player()[1].get("Camera3D").plane.y:.1f}"
                if self.world.get_player()[1].get("Camera3D") else None
            )
        )
        #-------------------------------------#
        pg.event.set_grab(configs.game.lock_mouse)
        pg.mouse.set_visible(configs.game.visible_mouse)
    #=====================================#
    def get_delta_time(self) -> float:
        now = time.time()
        dt = now - self.prev_time
        self.prev_time = now
        return dt
    #=====================================#
    def pass_time(self, dt:float) -> float:
        self.time += dt * 1000
        return self.time
    #=====================================#
    def show_time(self, concatenate=False):
        #-------------------------------------#
        if not concatenate:
            return self.time
        #-------------------------------------#
        total_ms = int(self.time)
        #-------------------------------------#
        hours = total_ms // (60 * 60 * 1000)
        total_ms %= (60 * 60 * 1000)
        #-------------------------------------#
        minutes = total_ms // (60 * 1000)
        minutes = f"0{minutes}" if minutes < 10 else minutes
        total_ms %= (60 * 1000)
        #-------------------------------------#
        seconds = total_ms // 1000
        seconds = f"0{seconds}" if seconds < 10 else seconds
        milliseconds = total_ms % 1000
        #-------------------------------------#
        return (
            f"{hours}:"
            f"{minutes}:"
            f"{seconds}."
            f"{milliseconds}"
        )
    #=====================================#
    def lock_mouse(self):
        #-------------------------------------#
        if not configs.game.lock_mouse:
            return
        #-------------------------------------#
        x,y = pg.mouse.get_pos()
        #-------------------------------------#
        if x < configs.settings.window_size[0] * .3 or x > configs.settings.window_size[0] * .7:# or y > configs.settings.window_size[1]//2 or y < configs.settings.window_size[1]//2:
            pg.mouse.set_pos(configs.settings.window_size[0]//2, configs.settings.window_size[1]//2)
    #=====================================#
    def run(self):
        #=====================================#
        while self.running:
            #-------------------------------------#
            self.dt = self.get_delta_time()
            #--------------------------------#
            if self.dt < configs.engine.max_delta_time_value:
                self.pass_time(self.dt)
            #-------------------------------------#
            self.running = self.events_handler.handle_events()
            #-------------------------------------#
            self.updater.update(self.dt)
            self.render.draw(self.screen, self.main_surface, self.dt)
            self.world.flush()
            #-------------------------------------#
            self.lock_mouse()
            #-------------------------------------#
            if configs.settings.show_fps_in_title:
                pg.display.set_caption(f"{configs.game.window_title} | {self.clock.get_fps():.1f}")
            #-------------------------------------#
            # debug_log(f"{assetsmarks.engine.debug}::overlay.fps", 
            #         value=f"{self.clock.get_fps():.1f}"
            #         )
            # #-------------------------------------#
            pg.display.update()
            self.clock.tick(configs.settings.max_fps)

#=====================================#
if __name__ == "__main__":
    main = Main()
    main.run()

