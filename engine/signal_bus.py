from engine.configs.configs import configs
from engine.utils.log import log, log_error, log_list
from engine.utils.debug_log import debug_log
#================================#
from game.enums.assets_marks import assetsmarks
#================================#
import inspect
from collections import deque
#================================#
class SignalBus:
    #================================#
    def __init__(self):
        #--------------------------------#
        self.listeners = {}  # signal: [(priority, callback, origin)]
        self.queue = deque()
        #--------------------------------#
        # debug_log(f"{assetsmarks.engine.debug}::signal_bus.show_", 
        #           value=self.atlas.groups_data)
    #================================#
    def clear(self):
        #--------------------------------#
        self.listeners = {}
        self.queue = deque()
        #--------------------------------#
        value = f"![ev_bus]: bus cleaned"
        debug_log(f"{assetsmarks.engine.debug}::signal_bus.show_unsubscribed", 
                    value=value)

    #================================#
    def subscribe(self, signal:str, callback, origin=None, priority:int=0):
        #--------------------------------#
        if origin is None:
            _build_origin(callback)
        #--------------------------------#
        self.listeners.setdefault(signal, []).append(
            (priority, callback, origin)
        )
        #--------------------------------#
        value = f"[ev_bus]: subscribed signal:{signal}, callback:{callback}, origin:{origin}, priority:{priority}"
        debug_log(f"{assetsmarks.engine.debug}::signal_bus.show_subscribed", 
                  value=value)
    #================================#
    def unsubscribe(self, callback, signal: str):
        #--------------------------------#
        if signal in self.listeners:
            self.listeners[signal] = [
                (p, cb, o)
                for p, cb, o in self.listeners[signal]
                if cb != callback
            ]
            #--------------------------------#
            if not self.listeners[signal]:
                del self.listeners[signal]
            #--------------------------------#
            value = f"[ev_bus]: unsubscribed callback:{callback} from signal:{signal}"
            debug_log(f"{assetsmarks.engine.debug}::signal_bus.show_unsubscribed", 
                    value=value)
            #--------------------------------#
            return
            
        log_error(f"signal: {signal} is not subscribbed", True)
    #================================#
    def unsubscribe_func(self, callback):
        for signal in list(self.listeners.keys()):
            #--------------------------------#
            self.listeners[signal] = [
                (p, cb, o)
                for p, cb, o in self.listeners[signal]
                if cb != callback
            ]
            #--------------------------------#
            if not self.listeners[signal]:
                del self.listeners[signal]
        #--------------------------------#
        value = f"[ev_bus]: unsubscribed callback:{callback} from all signals"
        debug_log(f"{assetsmarks.engine.debug}::signal_bus.show_unsubscribed", 
                    value=value)

    #================================#
    def unsubscribe_signal(self, signal: str):
        self.listeners.pop(signal, None)
        #--------------------------------#
        value = f"[ev_bus]: unsubscribed signal:{signal} from bus"
        debug_log(f"{assetsmarks.engine.debug}::signal_bus.show_unsubscribed", 
                    value=value)

    #================================#
    def unsubscribe_origin(self, origin: str):
        #--------------------------------#
        for signal in list(self.listeners.keys()):
            #--------------------------------#
            self.listeners[signal] = [
                (p, cb, o)
                for p, cb, o in self.listeners[signal]
                if o != origin
            ]
            #--------------------------------#
            if not self.listeners[signal]:
                del self.listeners[signal]
        #--------------------------------#
        value = f"[ev_bus]: unsubscribed all functions from origin {origin}"
        debug_log(f"{assetsmarks.engine.debug}::signal_bus.show_unsubscribed", 
                    value=value)

    #================================#
    def emit(self, signal: str, **data):
        self.queue.append((signal, data))
        #--------------------------------#
        if signal in configs.debug.signal_bus.emit.ignore_signals:         
            return
        #--------------------------------#
        value = f"[ev_bus]: emited signal:{signal} with data{data}"
        debug_log(f"{assetsmarks.engine.debug}::signal_bus.emit", 
                    value=value)

    #================================#
    def process(self):
        while self.queue:
            #--------------------------------#
            signal, data = self.queue.popleft()
            #--------------------------------#
            for _, callback, origin in self.listeners.get(signal, [])[:]:
                #--------------------------------#
                self.listeners[signal].sort(
                    key=lambda x: x[0],
                    reverse=False
                )
                #--------------------------------#
                try:
                    if "entity_data" in data:
                        callback(
                            data["entity"],
                            **data["entity_data"]
                        )
                    else:
                        callback(**data)
                    #--------------------------------#
                    if signal not in configs.debug.signal_bus.emit.ignore_signals:         
                        value = f"[ev_bus]: callback executed:{callback} with origin{origin}"
                        debug_log(f"{assetsmarks.engine.debug}::signal_bus.callback_executed", 
                                    value=value)
                #--------------------------------#
                except Exception as e:
                    log_error(
                        f"Error on callback {callback}, "
                        f"with data {data}"
                    )
                    log_error(e)

#--------------------------------#
# decorator
def subscribe(signal: str = "None", origin: str = None):
    #--------------------------------#
    def decorator(func):
        func.__signal__ = signal
        if origin is None:
            origin = _build_origin(func)
        func.__origin__ = origin
        return func
    #--------------------------------#
    return decorator
#--------------------------------#
def _build_origin(callback):
    #--------------------------------#
    try:
        #--------------------------------#
        file = inspect.getsourcefile(callback)
        line = inspect.getsourcelines(callback)[1]
        #--------------------------------#
        qualname = getattr(
            callback,
            "__qualname__",
            callback.__name__
        )
        #--------------------------------#
        return f"{qualname} ({file}:{line})"
    #--------------------------------#
    except Exception:
        return repr(callback)
#--------------------------------#
signal_bus = SignalBus()
