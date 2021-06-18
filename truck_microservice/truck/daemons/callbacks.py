"""[Docstring] Declares subscriber exceptions."""
from paho.mqtt.client import MQTTMessage # irgendwo spakkt der bei mir (Alexander) mit dem Import rum... gleich mal gucken https://pypi.org/project/paho-mqtt/

class Callbacks:
    """[Docstring] Declares callback functions and holds actual heartbeat."""

    heartbeat: int

    @staticmethod
    def on_message(client, userdata, msg: MQTTMessage) -> None:
        """[Docstring] Declares functions, handling message callback."""
        payload = msg.payload
        payload = payload.hex(':', 2)
        tick: float = 0
        tick = int(payload, base=16)
        Callbacks.heartbeat = tick
        print(tick)
      #   while True:
      #       if tick % 2 == 1:
      #           Movement(duration=0.05)
      #       else:
      #           Lifecycle()
