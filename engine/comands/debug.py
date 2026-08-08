from engine.console import command, console
from engine.configs.configs import configs
from engine.signal_bus import signal_bus
#-----------------------#
@command("debug.save", protection_level=0)
def debuf_save():
    configs.debug.save()
@command("debug.list", protection_level=0)
def debug_list():
    result = []
    #-----------------------#
    def scan(node, path=""):
        #-----------------------#
        for key, value in node.__dict__.items():
            #-----------------------#
            if key.startswith("_"):
                continue
            #-----------------------#
            new_path = f"{path}.{key}" if path else key
            #-----------------------#
            if hasattr(value, "do_debug"):
                result.append(new_path)
            #-----------------------#
            if hasattr(value, "__dict__"):
                scan(value, new_path)
    #-----------------------#
    scan(configs.debug)
    #-----------------------#
    console.log_list(
        result,
        list_name="debug options",
        list_color="white"
    )
    #-----------------------#
    return f"{len(result)} debug options found"
#-----------------------#
@command("debug.enable", protection_level=1)
def debug_enable(path:str):
    #-----------------------#
    target = configs.debug.get_path(path)
    #-----------------------#
    if target is None:
        console.log_error("debug '{path}' not found")
    #-----------------------#
    target.do_debug = True
    #-----------------------#
    return f"{path} enabled"
#-----------------------#
@command("debug.disable", protection_level=1)
def debug_disable(path:str):
    #-----------------------#
    target = configs.debug.get_path(path)
    #-----------------------#
    if target is None:
        console.log_error(f"debug '{path}' not found")
    #-----------------------#
    target.do_debug = False
    #-----------------------#
    return f"{path} disabled"
#-----------------------#
@command("debug.toggle", protection_level=1)
def debug_toggle(path:str):
    #-----------------------#
    target = configs.debug.get_path(path)
    #-----------------------#
    if target is None:
        console.log_error(f"debug '{path}' not found")
    #-----------------------#
    target.do_debug = not target.do_debug
    #-----------------------#
    return f"{path}: {target.do_debug}"
#-----------------------#
@command("debug.info", protection_level=0)
def debug_info(path:str):
    #-----------------------#
    target = configs.debug.get_path(path)
    #-----------------------#
    if target is None:
        return f"debug '{path}' not found"
    #-----------------------#
    console.log_dict(
        target._data,
        value_color="white",
        dict_name=path,
        name_color="cyan"
    )
#-----------------------#
@command("debug.all", protection_level=2)
def debug_all(state:bool):
    #-----------------------#
    def apply(node):
        #-----------------------#
        if hasattr(node, "do_debug"):
            node.do_debug = state
        #-----------------------#
        for value in node.__dict__.values():
            if hasattr(value, "__dict__"):
                apply(value)
    #-----------------------#
    apply(configs.debug)
    #-----------------------#
    return f"all debug set to {state}"
#-----------------------#
@command("debug.console.enable", protection_level=1)
def debug_console_enable(path:str):
    #-----------------------#
    target = get_debug_target(path)
    target.show_on_console = True
    #-----------------------#
    return f"{path} enabled on console"
#-----------------------#
@command("debug.console.disable", protection_level=1)
def debug_console_disable(path:str):
    #-----------------------#
    target = get_debug_target(path)
    #-----------------------#
    target.show_on_console = False
    #-----------------------#
    return f"{path} disabled on console"
#-----------------------#
@command("debug.overlay.enable", protection_level=1)
def debug_overlay_enable(path:str):
    #-----------------------#
    target = get_debug_target(path)
    #-----------------------#
    target.show_on_overlay = True
    #-----------------------#
    return f"{path} enabled on overlay"
#-----------------------#
@command("debug.overlay.disable", protection_level=1)
def debug_overlay_disable(path:str):
    #-----------------------#
    target = get_debug_target(path)
    #-----------------------#
    target.show_on_overlay = False
    #-----------------------#
    return f"{path} disabled on overlay"
#-----------------------#
@command("debug.display.toggle", protection_level=1)
def debug_display_toggle(path:str, display:str):
    #-----------------------#
    target = get_debug_target(path)
    #-----------------------#
    if display == "console":
        target.show_on_console = not target.show_on_console
        #-----------------------#
        return (
            f"{path} console: "
            f"{target.show_on_console}"
        )
    #-----------------------#
    if display == "overlay":
        target.show_on_overlay = not target.show_on_overlay
        #-----------------------#
        return (
            f"{path} overlay: "
            f"{target.show_on_overlay}"
        )
    #-----------------------#
    return (
        "display must be "
        "'console' or 'overlay'"
    )
#-----------------------#
@command("debug.display.info", protection_level=0)
def debug_display_info(path:str):
    #-----------------------#
    target = get_debug_target(path)
    #-----------------------#
    console.log_dict(
        {
            "do_debug": target.do_debug,
            "console": target.show_on_console,
            "overlay": target.show_on_overlay
        },
        dict_name=path,
        name_color="cyan"
    )
#-----------------------#
def get_debug_target(path:str):
    target = configs.debug.get_path(path)
    #-----------------------#
    if target is None:
        raise ValueError(
            f"debug '{path}' not found"
        )
    #-----------------------#
    if not hasattr(target, "do_debug"):
        raise ValueError(
            f"'{path}' is not a debug option"
        )
    #-----------------------#
    return target

