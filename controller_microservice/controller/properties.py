"""Some values the truck needs to know about the network (Self, Convoy, Admin-Service, and MQTT)"""
# Network Identification: As Subscriber of MQTT Broker -> fixed
ID_BROKER = 'monitorSubscriber'
ADDRESS_BROKER = '127.0.0.1'
PORT_BROKER = 1883
USERNAME_BROKER = 'testUser'
PASSWORD_BROKER = 'test'
TOPIC_BROKER = 'monitorChannel'
DURATION_BROKER = 0.025
