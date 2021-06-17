"""[Docstring] Declares subscriber exceptions."""
from paho.mqtt.client import MQTTMessage # irgendwo spakkt der bei mir (Alexander) mit dem Import rum... gleich mal gucken https://pypi.org/project/paho-mqtt/
from threading import Thread
from .movement import Movement
from .lifecycle import Lifecycle

class Callbacks:
    """[Docstring] Declares callback functions and holds actual heartbeat."""

    heartbeat: float
    
    @staticmethod
    def on_message(client, userdata, msg: MQTTMessage) -> None:
        """[Docstring] Declares functions, handling message callback."""
        payload = msg.payload
        payload = payload.hex(':', 2)
        tick: float = 0
        tick = int(payload, base=16)
        Callbacks.heartbeat = tick
        while True:
            if tick % 2 == 1:
                Movement(duration=0.25)
            else:
                Lifecycle()
