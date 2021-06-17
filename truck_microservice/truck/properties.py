"""Some values the truck needs to know about the network (Convoy, Admin-Service, and Broker)"""

# Network Identification: Truck (self) Microservice -> depending on truck
ID = 151
ADDRESS_SELF = '127.0.0.1:1031'

# Network Identification: Convoy Microservice -> fixed
ADDRESS_CONVOY = '127.0.0.1:1030'
ADDRESS_BROKER = '127.0.0.1'

# Network Identification: Admin Microservice -> fixed
ADDRESS_ADMIN = '127.0.0.1:1029'

# Network Identification: MQTT Broker -> fixed
PORT_BROKER = 1028
USER_BROKER = 'testUser'
PASSWORD_BROKER = 'test'
CHANNEL_BROKER = 'truckChannel'
DURATION_BROKER = 0.025

# Truck specific properties: Truck physics -> fixed
MIN_SPEED = 0.0
MAX_SPEED = 22.22222222222222

# Truck specific properties: Truck physics and calculation -> depending on truck
MIN_ACCELERATION = -3.0
MAX_ACCELERATION = 2.5
LENGTH = 18.0
DISTANCE = 0.5
DEPARTURE_DISTANCE = 300.0
