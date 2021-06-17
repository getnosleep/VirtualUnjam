# Truck Microservice -> depending on service
ID = 151
ADDRESS_SELF = '127.0.0.1:1031'

# Address Microservice -> fixed
ADDRESS_CONVOY = '127.0.0.1:1030'
ADDRESS_BROKER = '127.0.0.1'

# Admin Microservice -> fixed
ADDRESS_ADMIN = '127.0.0.1:1029'

# MQTT Broker -> fixed
PORT_BROKER = 1028
USER_BROKER = 'testUser'
PASSWORD_BROKER = 'test'
CHANNEL_BROKER = 'truckChannel'
DURATION_BROKER = 0.025

# physical fixed props
MIN_SPEED = 0.0
MAX_SPEED = 22.22222222222222
MIN_ACCELERATION = -3.0
MAX_ACCELERATION = 2.5
EMERGENCY_BRAKE = -2.5

# changeable props
LENGTH = 18.0
DISTANCE = 0.5
DEPARTURE_DISTANCE = 300.0
