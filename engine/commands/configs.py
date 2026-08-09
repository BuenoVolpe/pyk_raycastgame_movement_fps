from engine.console import command, console
from engine.configs.configs import configs
from engine.signal_bus import signal_bus
#-----------------------#
@command("configs.get", protection_level=0)
def get(config:str, key:str, default_value=None):
    """logs and prints a text at the console"""
    return configs.get(config, key, default_value)
#-----------------------#
@command("configs.set", protection_level=2)
def set(config:str, key:str, value):
    """logs and prints a text at the console"""
    configs.set(config, key, value)
    return f"changed {key} to {value} on configs {config}"
#-----------------------#
@command("configs.data", protection_level=2)
def data(config:str):
    """logs and prints a text at the console"""
    data = configs.get_data(config)
    console.log_dict(data, "black", dict_name=f"{config} data", name_color="white")
#-----------------------#

