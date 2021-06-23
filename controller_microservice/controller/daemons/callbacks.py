"""[Docstring] Declares subscriber exceptions."""
import json
from paho.mqtt.client import MQTTMessage

class Callbacks:
    """[Docstring] Declares callback functions and holds actual heartbeat."""
    truckDictionary: dict = {}
    
    @staticmethod
    def on_message(client, userdata, msg: MQTTMessage) -> None:
        """[Docstring] Declares functions, handling message callback."""
        sortedTrucksDict = {}
        payload = msg.payload
        truckDict: dict = json.loads(payload.decode('utf-8'))
        if not truckDict['position']:
            truckDict['position'] = -1
        trucksList = list(Callbacks.truckDictionary.values())
        trucksList.append(truckDict)
        for truck in trucksList:
            sortedTrucksDict[truck['id']] = truck
        Callbacks.truckDictionary = sortedTrucksDict
