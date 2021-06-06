"""[Docstring] Declares functions, handling mqtt subscription."""
"""[Docstring] Declares functions, handling mqtt subscription."""
import sys
from time import sleep
import paho.mqtt.client as mqtt

class MqttPublishService:
    """[Docstring] Declares functions, handling mqtt subscription."""

    countPub: float

    @staticmethod
    def on_publish(client: mqtt.Client, msg: mqtt.MQTTMessage):
        """[Docstring] Declares functions, handling message callback."""
        sleep(0.020)

if __name__=="__main__":
    MqttPublishService.countPub = 0
    client = mqtt.Client(client_id="heartbeatPublisher",
                            clean_session=False,
                            userdata=None,
                            protocol=mqtt.MQTTv311,
                            transport="tcp")
    client.username_pw_set('testUser', 'test')
    client.on_publish = MqttPublishService.on_publish
    client.connect("127.0.0.1", 1883, 60)
    while MqttPublishService.countPub >= 0:
        MqttPublishService.countPub += 1
        payload: bytes = MqttPublishService.countPub.to_bytes(2, "big")
        print(MqttPublishService.countPub)
        print(payload)
        client.publish("truckChannel", payload=payload, qos=0, retain=False, properties=None)