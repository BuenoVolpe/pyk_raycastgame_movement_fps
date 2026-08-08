import pygame as pg
#================================#
from engine.utils.log import log, log_error
#--------------------------------#
from engine.signal_bus import signal_bus
#--------------------------------#
from game.enums.inputs import inputsenum as inp
from game.enums.signals import signals
from game.enums.signals_prioritys import sig_prio
#--------------------------------#
from engine.console import console
#--------------------------------#
from engine.configs.configs import configs
from engine.configs.inputs import inputs
#================================#
class EventsHandler:
    #--------------------------------#
    def __init__(self, world):
        self.world = world
        #--------------------------------#
        self.objects = {}#priotity[objects]
    #=====================================#
    def _subscribe_functions(self):
        #-------------------------------------#
        signal_bus.subscribe(signals.EVENT_HANDLER_ADD_OBJECT, self.add_object, sig_prio.ADD_OBJ)
        signal_bus.subscribe(signals.EVENT_HANDLER_REMOVE_OBJECT, self.remove_object, sig_prio.REMOVE_OBJ)
    #=====================================#
    def handle_events(self):
        #--------------------------------#
        for event in pg.event.get():
            #--------------------------------#
            if event.type == pg.QUIT or (
                    # (event.type == pg.KEYDOWN and event.key == pg.K_LALT)
                    inputs.input_by_event(event, inp.FAST_QUIT, form="down")
                ):
                #--------------------------------#
                return self.quit()
            #------------------------------#
            elif event.type == pg.KEYDOWN:
                self.handle_keydown(event)
            elif event.type == pg.KEYUP:
                self.handle_keyup(event)
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.handle_mousedown(event)
            elif event.type == pg.MOUSEBUTTONUP:
                self.handle_mouseup(event)
            elif event.type == pg.MOUSEWHEEL:
                self.handle_mousewheel(event)
            #------------------------------#
            self.inputs(event)
            self.handle_object_events(event)
            #--------------------------------#
            signal_bus.emit(signals.PGEVENT, event=event)
        return True
    #================================#
    def inputs(self, event):
        #--------------------------------#
        if inputs.input_by_event(event, inp.ACTIVE_DEBUG_OVERLAY):
            signal_bus.emit(signals.ACTIVE_DEBUGOVERLAY)
        #--------------------------------#
        elif inputs.input_by_event(event, inp.CONSOLE_PGDOWN): 
            signal_bus.emit(signals.CONSOLE_PGDOW)
        elif inputs.input_by_event(event, inp.CONSOLE_PGUP): 
            signal_bus.emit(signals.CONSOLE_PGUP)
        #--------------------------------#
        elif inputs.input_by_event(event, inp.INTERACT):
            eid, comps = self.world.get_player()
            signal_bus.emit(signals.INTERACT, player_eid=eid, player_comps=comps)
        #--------------------------------#
        elif inputs.input_by_event(event, inp.ACTIVE_CONSOLE): 
            if configs.console.can_active and configs.console.can_active_by_hotkey:
                #--------------------------------#
                console.visible = not console.visible
                #--------------------------------#
                # cmd_string = inputs.pyinput("> ") 
                # signal_bus.emit(signals.EXECUTE_COMMAND, string=cmd_string)
        elif inputs.input_by_event(event, inp.MENU): 
            console.visible = False
    #================================#
    def handle_object_events(self, event):
        #------------------------------#
        for priority in sorted(self.objects.keys()):
            for obj in self.objects[priority]:
                #------------------------------#
                if hasattr(obj, "handle_event"):
                    obj.handle_event(event)
                    continue
                #------------------------------#
                if hasattr(obj, "handle_events"):
                    obj.handle_events(event)
                    continue
                #------------------------------#
                if hasattr(obj, "events"):
                    obj.events(event)
                    continue
                #------------------------------#
                log_error(f"Object {obj.__class__.__name__} does not have handle_event or handle_events or events method.")
        #------------------------------#
        console.handle_event(event)
    #================================#
    def handle_keydown(self, event):
        #------------------------------#
        signal_bus.emit(signals.PGEVENT_KEY_DOWN, event=event)
        #------------------------------#
    #================================#
    def handle_keyup(self, event):
        #------------------------------#
        signal_bus.emit(signals.PGEVENT_KEY_UP, event=event)
    #================================#
    def handle_mousedown(self, event):
        #------------------------------#
        signal_bus.emit(signals.PGEVENT_MOUSE_DOWN, event=event)
    #================================#
    def handle_mouseup(self, event):
        #------------------------------#
        signal_bus.emit(signals.PGEVENT_MOUSE_UP, event=event)
    #=====================================#
    def handle_mousewheel(self, event):
        if console.visible:
            return
        #------------------------------#
        signal_bus.emit(signals.PGEVENT_MOUSE_WHEEL, event=event)
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
    #================================#
    def quit(self):
        #--------------------------------#
        pg.quit()
        exit()
        return False
#--------------------------------#

