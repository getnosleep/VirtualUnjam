"""Some values the publisher needs, to determine where and when to publish data"""
from paho.mqtt.client import MQTTv311

# Network Identification: MQTT Broker (self) -> fixed
ID = 'heartbeatPublisher'
INTERVAL = 0.025
ADDRESS = '127.0.0.1'
PORT = 1028
USERNAME = 'testUser'
PASSWORD = 'test'

# Heartbeat settings: MQTT Publisher (self) -> fixed
MESSAGE_PROTOCOL = MQTTv311 # Current standard of MQTT-Messaging    -> not necessary, because it is a standard setting
CONNECTION_PROTOCOL = 'tcp' # Standard for MQTT-Connection          -> not necessary, because it is a standard setting
QUALITY_OF_SERVICE = 0      # (qos) Unnested Messages               -> not necessary, because it is a standard setting
BYTEORDER = 'big'           # Big-Endian                            -> necessary
PAYLOAD_LENGTH = 8          # 8 Bytes = 64 bit                      -> necessary
TOPIC = 'truckChannel'      # A channel for subscribers             -> necessary
