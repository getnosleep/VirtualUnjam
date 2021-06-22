"""Some values the truck needs to know about the network (Self, Convoy, Admin-Service, and MQTT)"""
# Network Identification: Truck (self) Microservice -> depending on truck
ID = 151
ADDRESS_SELF = '127.0.0.1:1031'

# Network Identification: Convoy Microservice -> fixed
ADDRESS_CONVOY = '127.0.0.1:1030'

# Network Identification: Admin Microservice -> fixed
ADDRESS_ADMIN = '127.0.0.1:1029'

# Network Identification: As Subscriber of MQTT Broker -> fixed
ID_BROKER = 'heartbeatPublisher'
ADDRESS_BROKER = '127.0.0.1'
PORT_BROKER = 1883
USERNAME_BROKER = 'testUser'
PASSWORD_BROKER = 'test'
TOPIC_HEARTBEAT = 'truckChannel'
TOPIC_MONITOR = 'monitorChannel'
DURATION_BROKER = 0.025

# Network specific settings: Request settings -> fixed
MAX_TIMEOUT = 0.5

# Truck specific properties: Truck physics -> fixed
MIN_SPEED = 0.0
MAX_SPEED = 22.22222222222222

# Truck specific properties: Truck physics and calculation -> depending on truck
MIN_ACCELERATION = -3.0
MAX_ACCELERATION = 2.5
LENGTH = 18.0
DISTANCE = 0.5
DEPARTURE_DISTANCE = 300.0
