from engine.console import command, console
from engine.configs.configs import configs
#-----------------------#
@command("say", protection_level=0)
def say(text:str="hello, world!"):
    """logs and prints a text at the console"""
    return text

    