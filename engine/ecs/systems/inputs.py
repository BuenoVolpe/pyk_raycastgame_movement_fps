from game.ecs.components.all import Inputs, PlayerTag, Velocity
from engine.utils.scaler import scaler
from engine.configs.configs import configs
#--------------------------------#
from engine.signal_bus import signal_bus
from game.enums.signals import signals
from game.enums.signals_prioritys import sig_prio
#================================#
inputs = configs.inputs
#================================#
class InputSystem:
    #--------------------------------#
    def __init__(self, world:object):
        #--------------------------------#
        self.world = world

    #================================#
    def update(self, *args):
        #--------------------------------#
        for entity, (inp, vel, tag) in self.world.query(Inputs, Velocity, PlayerTag):
            #--------------------------------#
            from engine.configs.inputs import inputs
            #--------------------------------#
            has_something_pressed = False
            for key in inp.inputs.keys():
                inp.inputs[key] = bool(inputs.input(key))
                inp._reload()
                #--------------------------------#
                if inp.inputs[key]:
                    has_something_pressed = True
                    signal_bus.emit(signals.INPUT, entity=entity, inp=key)
                #--------------------------------#
            if not has_something_pressed:
                signal_bus.emit(signals.NO_INPUT, entity=entity)
            #--------------------------------#
            if tag.USE_NORMAL_VEL_SYSTEM:
                speed = [0,0]
                #--------------------------------#
                if inp.inputs.get("up", False):
                    speed[1] = -vel.max.y
                if inp.inputs.get("down", False):
                    speed[1] = vel.max.y
                if inp.inputs.get("left", False):
                    speed[0] = -vel.max.x
                if inp.inputs.get("right", False):
                    speed[0] = vel.max.x
                #--------------------------------#
                vel.x = speed[0]
                vel.y = speed[1]
            #--------------------------------#
            inp._reload()
