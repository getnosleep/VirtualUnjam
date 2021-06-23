"""Some values the truck needs to know about the network (Self, Convoy, Admin-Service, and MQTT)"""
# Network Identification: As Subscriber of MQTT Broker -> fixed
COUNT = 0
INTERVAL = 0.1
ID_BROKER = 'monitorSubscriber'
ADDRESS_BROKER = '127.0.0.1'
PORT_BROKER = 1883
USERNAME_BROKER = 'testUser'
PASSWORD_BROKER = 'test'
TOPIC_BROKER = 'monitorChannel'
TOPIC_TRUCKS = 'truckChannel'
DURATION_BROKER = 0.025
MAX_TIMEOUT = 60
ADDRESS_HEARTBEAT = '127.0.0.1:1028'
