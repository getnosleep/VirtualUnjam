"""[Docstring] Declares subscriber exceptions."""
from paho.mqtt.client import MQTTMessage

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
