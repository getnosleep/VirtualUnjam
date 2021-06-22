"""[Docstring] Declares subscriber exceptions."""
from .lifecycle import alive
from .movement import move
from paho.mqtt.client import MQTTMessage

class Callbacks:
    """[Docstring] Declares callback functions and holds actual heartbeat."""

    heartbeat: float
    
    @staticmethod
    def on_message(client, userdata, msg: MQTTMessage) -> None:
        """[Docstring] Declares functions, handling message callback."""
        payload = msg.payload
        tick = int.from_bytes(payload, "big")
        Callbacks.heartbeat = tick
        if tick%2 == 0:
            move()
        elif tick%2 == 1:
            alive()
