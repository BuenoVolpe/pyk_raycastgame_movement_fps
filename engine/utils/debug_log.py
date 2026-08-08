from engine.configs.configs import configs
#--------------------------------#
from engine.utils.log import log, log_error, log_list, log_dict, log_success
from engine.utils.dict_to_class import dict_to_class
#================================#
def debug_log(debug_name:str, value:any, **kwargs):
    #--------------------------------#
    kwargs = dict_to_class(kwargs) or dict_to_class({})
    #--------------------------------#
    debug = configs.debug 
    #================================#
    debug_string = debug_name.split("::")    
    if len(debug_string) != 2:
        log_error(f"invalid debug string: {debug_name}")
        return
    debug_string = debug_string[1]
    #--------------------------------#
    full_name = debug_string.split(".")
    if len(full_name) != 2:
        log_error(f"invalid debug string: {debug_name}")
        return
    obj, name = full_name
    # #--------------------------------#
    obj_data = debug.get(obj, {})
    #--------------------------------#
    if not obj_data:
        log_error(f"cant find object in {debug_name}")
        return
    #--------------------------------#
    debug_data = obj_data.get(name, {})
    if not debug_data:
        log_error(f"cant find debug data in {debug_name}")
        return
    #================================#
    if not debug_data.do_debug:
        return
    #================================#
    color = debug_data.get("color") if kwargs.get("color") is None else kwargs.get("color", "black")
    styles = debug_data.get("styles") if kwargs.get("styles") is None else kwargs.get("styles", [])
    console = debug_data.get("console") if kwargs.get("console") is None else kwargs.get("console", None)
    list_name = debug_data.get("list_name") if kwargs.get("list_name") is None else kwargs.get("list_name", "")
    list_color = debug_data.get("list_color") if kwargs.get("list_color") is None else kwargs.get("list_color", "white")
    key_color = debug_data.get("key_color") if kwargs.get("key_color") is None else kwargs.get("key_color", "yellow")
    value_color = debug_data.get("value_color") if kwargs.get("value_color") is None else kwargs.get("value_color", "white")
    styles = debug_data.get("styles") if kwargs.get("styles") is None else kwargs.get("styles", [])
    list_styles = debug_data.get("list_styles") if kwargs.get("list_styles") is None else kwargs.get("list_styles", [])
    dict_name = debug_data.get("dict_name") if kwargs.get("dict_name") is None else kwargs.get("dict_name", "")
    name_color = debug_data.get("name_color") if kwargs.get("name_color") is None else kwargs.get("name_color", "white")
    name_styles = debug_data.get("name_styles") if kwargs.get("name_styles") is None else kwargs.get("name_styles", [])
    name_in_overlay = debug_data.get("name_in_overlay", full_name) if kwargs.get("name_in_overlay") is None else kwargs.get("name_in_overlay", full_name)
    # #--------------------------------#
    # debug_data = dict_to_class(debug_data)
    #--------------------------------#
    match debug_data.log_type:
        #--------------------------------#
        case "log":
            log(value, color, styles, console)
        case "list":
            log_list(value, color, styles, list_name, list_color, list_styles, console)
        case "error":
            log_error(value, console)
        case "dict":
            log_dict(value, key_color, value_color, styles, dict_name, name_color, name_styles, console)
        case "succes":
            log_success(value, console)
        #--------------------------------#
        case "overlay":
            #--------------------------------#
            from engine.signal_bus import signal_bus
            from game.enums.signals import signals
            #--------------------------------#
            category = debug_data.get("category", "Others")
            #--------------------------------#
            data = DebugValue(
                value=value,
                color=color,
                category=category,
                order=debug_data.get("order",0),
                formatter=debug_data.get("formatter",None)
            )
            #--------------------------------#
            signal_bus.emit(signals.ADD_TO_OVERLAY, data=data, name=name_in_overlay)
#================================#
class DebugValue:
    #--------------------------------#
    def __init__(self, value, color, category, order=0, formatter=None, history=False):
        #--------------------------------#
        self.value = value
        self.color = color
        self.category = category
        self.order = order
        self.formatter = formatter
        self.history = history
#================================#

