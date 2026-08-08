#=====================================#
import pygame as pg
#=====================================#
from engine.utils.log import log_error
#--------------------------------#
from game.ecs.systems.all import *
#--------------------------------#
from engine.signal_bus import signal_bus
from game.enums.signals import signals
from game.enums.signals_prioritys import sig_prio
#--------------------------------#
from engine.configs.configs import configs
#=====================================#
class Updater:
    #=====================================#
    def __init__(self, world, grid):
        self.world = world
        self.grid = grid
        #--------------------------------#
        self.objects = {} #priority: [elements]
        #--------------------------------#
        self.systems = [ #[sys1, sys2(value, key), sys3(kwarg="aa")]
            SimpleAnimationSystem(self.world),
            StateAnimationSystem(self.world),
            LookingAtEntitySystem(self.world),
            ThinWallUpdateSystem(self.world),
            DoorUpdateSystem(self.world),
            Sprites3DSystem(self.world),
            MouseLookSystem(self.world),
            Raycaster3DCameraSystem(self.world),
            InputSystem(self.world),
            PlayerSignals(self.world),
            LookAtSystem(self.world),
            VisualRotationSystem(self.world),
            GridCollisionSystem(self.world, grid),
            MovementSystem(self.world),
            AngularMovementSystem(self.world),
        ] 
        #=====================================#
        self._subscribe_functions()
    #=====================================#
    def _subscribe_functions(self):
        #-------------------------------------#
        signal_bus.subscribe(signals.UPDATER_ADD_OBJECT, self.add_object, sig_prio.ADD_OBJ)
        signal_bus.subscribe(signals.UPDATER_REMOVE_OBJECT, self.remove_object, sig_prio.REMOVE_OBJ)
    #=====================================#
    def update(self, delta_time:float):
        #--------------------------------#
        if delta_time > configs.engine.max_delta_time_value:
            return
        #--------------------------------#
        signal_bus.emit(signals.ENGINE_UPDATE, dt=delta_time)
        #--------------------------------#
        signal_bus.process()
        #--------------------------------#
        for system in self.systems:
            system.update(delta_time)
        #--------------------------------#
        for priority in sorted(self.objects.keys()):
            for obj in self.objects[priority]:
                #--------------------------------#
                if hasattr(obj, "update"):
                    obj.update(delta_time)
                    continue
                #--------------------------------#
                log_error(f"Object {obj} has no 'update' method.")
    #=====================================#
    def add_object(self, obj:object, priority:int=0):
        #--------------------------------#  
        if priority not in self.objects:
            self.objects[priority] = []
        #--------------------------------#
        self.objects[priority].append(obj)
    #--------------------------------#
    def remove_object(self, obj:object):
        for priority in self.objects:
            if obj in self.objects[priority]:
                self.objects[priority].remove(obj)
                return
