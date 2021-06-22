"""[Docstring] Declares subscriber exceptions."""
import json
from paho.mqtt.client import MQTTMessage

class Callbacks:
    """[Docstring] Declares callback functions and holds actual heartbeat."""

    truckDictionary = {}
    
    @staticmethod
    def on_message(client, userdata, msg: MQTTMessage) -> None:
        """[Docstring] Declares functions, handling message callback."""
        payload = msg.payload
        truckDict = json.loads(payload.decode('utf-8'))

        # Auflistung nach ID -> Reihenfolge nach position

        position = truckDict['position']
        Callbacks.truckDictionary[position] = truckDict
