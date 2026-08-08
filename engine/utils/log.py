from colorama import Fore, Style, init
#================================#
init(autoreset=True)
#================================#
styles_dict = {
    "bright":Style.BRIGHT,
    "underline":Style.UNDERLINE
}
#--------------------------------#
colors_dict = {
    "BLACK": Fore.BLACK,
    "RED": Fore.RED,
    "GREEN": Fore.GREEN,
    "YELLOW": Fore.YELLOW,
    "BLUE": Fore.BLUE,
    "MAGENTA": Fore.MAGENTA,
    "CYAN": Fore.CYAN,
    "WHITE": Fore.WHITE,
    #--------------------------------#
    #extras
    # "LIGHTBLACK": Fore.LIGHTBLACK_EX,
    # "LIGHTRED": Fore.LIGHTRED_EX,
    # "LIGHTGREEN": Fore.LIGHTGREEN_EX,
    # "LIGHTYELLOW": Fore.LIGHTYELLOW_EX,
    # "LIGHTBLUE": Fore.LIGHTBLUE_EX,
    # "LIGHTMAGENTA": Fore.LIGHTMAGENTA_EX,
    # "LIGHTCYAN": Fore.LIGHTCYAN_EX,
    # "LIGHTWHITE": Fore.LIGHTWHITE_EX
}
#================================#
def log(text:str, color:str=None, styles:list[str|None, str|None]=[], console:object|None=None):
    #--------------------------------#
    #style
    styles = styles or []
    final_style = ""
    for style in styles:
        final_style += styles_dict.get(style, "")
    #--------------------------------#
    #color
    color = color or "BLACK"
    color_ = colors_dict.get(color.upper(), "BLACK")
    #--------------------------------#
    if not isinstance(text, str):
        text = str(text)
    #--------------------------------#
    print(color_ + final_style + text)
    #--------------------------------#
    if console:
        if not hasattr(console, "core"):
            from engine.console import console
            console.log(text, color, styles)
            return
        console.log(text, color, styles)
#================================#
def log_error(text:str, console:object|None=None):
    #--------------------------------#
    log(f"!> {text}", "red", ["bright", "underline"], console=False)
    #--------------------------------#
    if console:
        if not hasattr(console, "core"):
            from engine.console import console
            console.log_error(text)

            return
        console.log_error(text)
#================================#
def log_success(text:str, console:object|None=None):
    #--------------------------------#
    log(f">>[ {text} ]<<", "yellow", ["bright"], console=False)
    #--------------------------------#
    if console:
        if not hasattr(console, "core"):
            from engine.console import console
            console.log_success(text)
            return
        console.log_success(text)
#================================#
def log_list(list:list, color:str=None, styles:list[str|None, str|None]=[], list_name:str=None, list_color:str=None, list_styles:list[str|None, str|None]=[], console:object|None=None):
    #--------------------------------#
    if list_name:
        log(f"#========= {list_name} ==========#", list_color, list_styles, console)
    #--------------------------------#
    for item in list:
        log(item, color, styles, console)

def log_dict(dict:dict,
             key_color:str=None, value_color:str=None,
             styles:list[str|None, str|None]=[],
             dict_name=None, name_color:str=None, name_styles:list[str|None, str|None]=None,
             console=None):
    #----------------------#
    if dict_name:
        log(f"#========= {dict_name} ==========#", name_color, name_styles, console)
    #----------------------#
    key_color = key_color or "BLACK"
    key_color = colors_dict.get(key_color.upper(), "BLACK")
    value_color = value_color or "BLACK"
    value_color = colors_dict.get(value_color.upper(), "BLACK")
    #----------------------#
    for key, value in dict.items():
        line = f"{key_color}> {key} {value_color}: {value},"
        log(line, None, styles, console)
#         if console:
# if not hasattr(console,:
    #   from engine.console import console
#     console.#()
#     return "core")
#             console.log(string, ...)






# log("aaaa")
# log("aaaa", "black")
# log("aaaa", "white", styles=["bright"])
# log("aaaa", "q", styles=["normal"])
# log("aaaa", "green", styles=["underline"])
# log("aaaa", "blue", styles=["bright", "underline"])
# log_error("aaaaa")
# log_success("aaaaa")
# log_list(["item1", "item2", "item3"], "cyan", ["bright"], list_name="My List")
