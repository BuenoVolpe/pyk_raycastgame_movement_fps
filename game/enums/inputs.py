#=====================================#
from engine.configs.configs import configs
#=====================================#
#=====================================#
class InputsEnum:
    #-------------------------------------#
    UP:str = "up"
    DOWN:str = "down"
    LEFT:str = "left"
    RIGHT:str = "right"
    #-------------------------------------#
    INTERACT:str = "interact"
    #-------------------------------------#    
    MENU:str = "menu"
    #-------------------------------------# 
    LMB:str = "LMB"
    RMB:str = "RMB"
    MMB:str = "MMB"
    TAB:str = "tab"
    #-------------------------------------#     
    FAST_QUIT:str = "fast_quit"
    ACTIVE_DEBUG_OVERLAY:str = "active_debug_overlay"
    ACTIVE_CONSOLE:str = "active_console"
    RESTART:str = "restart"
    #-------------------------------------#     
    CONSOLE_PGUP = "console_pgup"
    CONSOLE_PGDOWN = "console_pgdown"
#=====================================#
inputsenum = InputsEnum()
