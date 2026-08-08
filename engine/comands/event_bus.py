from engine.console import command, console
from engine.configs.configs import configs
from engine.signal_bus import signal_bus
#-----------------------#
@command("signal.emit", protection_level=2)
def emit(signal:str, **data):
    """emits a signal"""
    signal_bus.emit(signal, **data)
    return f"emitted {signal} with data: {data}"
#-----------------------#