"""[Docstring] Declares functions, handling mqtt subscription."""
from string import hexdigits
import struct
import sys
import paho.mqtt.client as mqtt
from struct import pack, unpack

class MqttSubscribeService:
    """[Docstring] Declares functions, handling mqtt subscription."""
    
    countSub: float

    @staticmethod
    def on_message(client, userdata, msg: mqtt.MQTTMessage):
        """[Docstring] Declares functions, handling message callback."""
        payload = msg.payload
        print(payload)
        payload = payload.hex(':', 2)
        print(payload)
        tick: float = 0
        tick = int(payload, base=16)
        MqttSubscribeService.countSub = tick
        print(MqttSubscribeService.countSub)

if __name__=="__main__":
    MqttSubscribeService.countSub = 0
    client = mqtt.Client(client_id="heartbeatSubscriber",
                            clean_session=False,
                            userdata=None,
                            protocol=mqtt.MQTTv311,
                            transport="tcp")
    client.username_pw_set('testUser', 'test')
    client.on_message = MqttSubscribeService.on_message
    client.connect("127.0.0.1", 1883, 60)
    client.subscribe("truckChannel", 0)
    client.loop_forever()
