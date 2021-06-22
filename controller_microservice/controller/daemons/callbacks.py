"""[Docstring] Declares subscriber exceptions."""
import json
from paho.mqtt.client import MQTTMessage

class Callbacks:
    """[Docstring] Declares callback functions and holds actual heartbeat."""

    truckDictionary: dict = {}
    
    @staticmethod
    def on_message(client, userdata, msg: MQTTMessage) -> None:
        """[Docstring] Declares functions, handling message callback."""
        sortedTrucksList = {}
        sortedTrucksDict = {}
        payload = msg.payload
        truckDict = json.loads(payload.decode('utf-8'))
        trucksList = list(Callbacks.truckDictionary.values())
        trucksList.append(truckDict)
        for i in trucksList:
            if not type(trucksList[i]['position']) == int:
                trucksList[i]['position'] = -1
        sortedTrucksList = sorted(trucksList, key=lambda k: k['position'])
        for truck in sortedTrucksList:
            sortedTrucksDict[truck['id']] = truck
        Callbacks.truckDictionary = sortedTrucksDict
