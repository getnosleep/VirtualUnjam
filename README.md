# VirtualUnjam @ https://github.com/getnosleep/VirtualUnjam
Microservices for a traffic simulation.
This project is created as a school project and can be used free.

Different truck-microservices are represented by the 'truck-microservice'. In combination with the Heartbeat Microservice,
the Address Microservice and a few small hints what to do, the trucks behave intelligent and prevent traffic jams.

## Software requirements
  - Python version 3.8.X
  - Mosquitto broker (recommended, otherwise mqtt-broker you can find) on port 1883

## PIP packages to install
  - django
  - djangorestframework
  - django-rest-swagger
  - paho-mqtt
  - validation



# How to start this project?
1. Install the required software (Python and Mosquitto)
  - Mosquitto mqtt-broker settings are set to 'Port 1883'. Either use this port or change the settings in tyhe 'properties.py's in this project

2. To install the needed pip packages, 'cd' to the 'requirements' file and start:
    `pip3 install -r requirements`

3. Copy the trucks microservice as many times as you want to have represented a truck in the system. This step is needed, because every truck has it's own database.
  - Change the 'properties.py' of every truck, so that it has a unique id and address/port
  - remember the port numbers, because it will be needed on start
  - recommendet ports for local start: 1031 and further

4. Starting Mosquitto broker by shell:
    `net start mosquitto`

5. Start the heartbeat broker on any port (Port 1028 recommended):
```
    cd heartbeat_microservice
    python manage.py runserver 1028
```

  - Tis service needs to be initialized by a POST request on 'http://{machine}:{port}/heartbeat/needle'
    JSON-payload:
```
    curl --location --request POST 'http://localhost:1028/heartbeat/needle' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "interval": 0.1,
        "count": 0,
        "broker_address": "127.0.0.1",
        "broker_port": 1883,
        "broker_username": "testUser",
        "broker_password": "test",
        "broker_channel": "truckChannel"
    }'
```

6. Start the address microservice on port 1030:
```
    cd address_microservice
    python manage.py runserver 1030
```

7. Start as many truck microservices as You created. Recommended ports are 1031 following, but use the ports defined in the 'properties.py' of every truck:
```
    cd truck_microservice
    python manage.py makemigrations truck
    python manage.py migrate truck
    python manage.py runserver {port}
```

8. To use the Website, start the controller service on any address:
```
    cd controller_microservice
    python manage.py runserver {port}
```
  - You should be able to see the trucks information on the web interface 'http://{machine}:{port}/api/web'

9. Manipulate the trucks by using the buttons and have fun (alternatively, make your own requests on curl / postman / etc. might work better :D )
