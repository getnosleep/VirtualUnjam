"""[Docstring] Declares subscriber exceptions."""
from .lifecycle import startLifecycle
from .movement import startMovement
from .drive import startDrive
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
        if tick%3 == 0:
            startLifecycle()
        elif tick%3 == 1:
            startDrive()
        elif tick%3 == 2:
            startMovement()
