from game.ecs.components.all import Inputs, PlayerTag, Velocity
from engine.utils.scaler import scaler
from engine.configs.configs import configs
#--------------------------------#
from engine.signal_bus import signal_bus
from game.enums.signals import signals
from game.enums.signals_prioritys import sig_prio
#================================#
from engine.ecs.components.all import States
#================================#
class PlayerSignals:
    def __init__(self, world):
        #--------------------------------#
        self.world = world
        #--------------------------------#
        for entity, (tag) in self.world.query(PlayerTag):
            self.player = entity
        #--------------------------------#
        self.subscribe()
    #================================#
    def subscribe(self):
        #--------------------------------#
        signal_bus.subscribe(signals.INPUT, self.change_state, priority=sig_prio.UPDATE_OBJ)
        signal_bus.subscribe(signals.NO_INPUT, self.change_state, priority=sig_prio.UPDATE_OBJ)
    #================================#
    def change_state(self, entity, inp=None):
        #--------------------------------#
        states = self.world.get_component(entity, States)
        #--------------------------------#
        if states is None:
            return
        #--------------------------------#
        if inp is None:
            #--------------------------------#
            current = states.current
            #--------------------------------#
            if "moving." in current:
                states.current = current.replace("moving.", "idle.")
            #--------------------------------#
            return
        #--------------------------------#
        states.current = f"ent_state@pyk::moving.{inp}"
    #================================#
    def update(self, *args):
        pass
    


