from engine.configs.configs import configs
#--------------------------------#
from engine.signal_bus import signal_bus
from engine.utils.debug_log import debug_log
from engine.utils.log import log_error
from game.enums.signals import signals
from game.enums.signals_prioritys import signals_prioritys
#--------------------------------#
from engine.handlers.fonts import fonts
#--------------------------------#
from engine.utils.dict_to_class import dict_to_class
from engine.utils.scaler import scaler
#================================#
class Overlay:
    #================================#
    def __init__(self):
        #--------------------------------#
        self.cfg = configs.debug.overlay
        #--------------------------------#
        self.actived = False
        #--------------------------------#
        self.watchers = {}
        self.values = {}
        #--------------------------------#
        signal_bus.subscribe(signals.ADD_TO_OVERLAY, self.set, priority=signals_prioritys.ADD_OBJ)
        signal_bus.subscribe(signals.ACTIVE_DEBUGOVERLAY, self.active, priority=signals_prioritys.UPDATE_UI)
    #================================#
    def active(self):
        self.actived = not self.actived
    #================================#
    def set(self, name:str, data:object):
        #--------------------------------#
        category = data.category
        #--------------------------------#
        if category not in self.values:
            self.values[category] = {}
        #--------------------------------#
        old = self.values[category].get(name)
        #--------------------------------#
        if old and old.value == data.value:
            return
        #--------------------------------#
        self.values[category][name] = data
    #================================#
    def watch(self, debug_name:str, callback, enable:bool=True):
        #--------------------------------#
        if not enable:
            return
        #--------------------------------#
        self.watchers[debug_name] = callback
    #================================#
    def update(self):
        #--------------------------------#
        for debug_name, callback in self.watchers.items():
            #--------------------------------#
            try:
                value = callback()
            #--------------------------------#
            except Exception as e:
                log_error(f"broken watcher in debug overlay at: {debug_name}, {callback}, \n exeption:{e}")
                continue
            #--------------------------------#
            debug_log(
                debug_name,
                value
            )
    #================================#
    def remove(self, name):
        #--------------------------------#
        for category in self.values.values():
            category.pop(name, None)
    #================================#
    def draw(self, screen):
        #--------------------------------#
        if not self.actived:
            return
        #--------------------------------#
        self.update()
        #--------------------------------#
        font = fonts.engine_default.get_size(self.cfg.font_size)
        #--------------------------------#
        x, y = scaler.coordenates(*self.cfg.coordenates)
        top = y
        #--------------------------------#
        _, y_padding = scaler.coordenates(0, self.cfg.y_padding)
        _, y_title_padding = scaler.coordenates(0, self.cfg.title_padding)
        #--------------------------------#
        column_width = 0
        #--------------------------------#
        categories = sorted(
            #--------------------------------#
            self.values.items(),
            #--------------------------------#
            key=lambda item:
                self.cfg.categorys
                .get(item[0], {})
                .get("order", 999)
        )
        #--------------------------------#
        for category_name, values in categories:
            #--------------------------------#
            category_cfg = dict_to_class(self.cfg.categorys.get(category_name))
            #--------------------------------#
            if category_cfg and not category_cfg.do_show:
                continue
            #--------------------------------#
            if category_name == "GameInfo":
                category_name = f"{category_name} || {configs.game.acronym}"
            elif category_name == "EngineInfo":
                category_name = f"{category_name} || {configs.engine.acronym}"
            #--------------------------------#
            fonts.engine_default.render(
                screen,
                (x, y),
                category_name,
                color=(255,255,0),
                size=self.cfg.font_size
            )
            #--------------------------------#
            y += y_padding
            #--------------------------------#
            values = sorted(
                #--------------------------------#
                values.items(),
                #--------------------------------#
                key=lambda item: item[1].order
            )
            #--------------------------------#
            for name, debug in values:
                value = self._format_value(debug)
                text = f"{name}: {value}"
                #--------------------------------#
                fonts.engine_default.render(
                    screen,
                    (x, y),
                    text,
                    color=debug.color,
                    size=self.cfg.font_size
                )
                #--------------------------------#
                width = font.size(text)[0]
                #--------------------------------#
                column_width = max(column_width, width)
                #--------------------------------#
                y += y_padding
                #--------------------------------#
                if y > screen.get_height() - y_padding:
                    #--------------------------------#
                    x += column_width + scaler.constant(25)
                    #--------------------------------#
                    y = top
                    #--------------------------------#
                    column_width = 0
            #--------------------------------#
            y += y_title_padding
    #================================#
    def _format_value(self, debug):
        #--------------------------------#
        value = debug.value
        #--------------------------------#
        if debug.formatter:
            value = debug.formatter(value)
        #--------------------------------#
        return value

debug_overlay = Overlay()
