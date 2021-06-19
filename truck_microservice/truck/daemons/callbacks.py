"""[Docstring] Declares subscriber exceptions."""
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
