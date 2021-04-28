"""[Docstring] Service class handling truck's driving behaviour."""
import requests
from typing import Final
from rest_framework import status
from .models import Truck
from validation import (
    validate_int, validate_float,
    validate_structure,
    validate_text,
)

class Drive(object):
    """[Docstring] Service class handling truck's driving behaviour.

    Functions:
        
        Static porperties' functions:

            setTrucksMaxSpeed(speed: float):

            getTrucksMaxSpeed(speed: float):float
        
        Truck's driving behaviour:

            changeSpeed(truckId: int, speed: float):boolean

            stopTruck(truckId: int):boolean

            changeConvoyPosition(truckId: int, newConvoyPosition: int):boolean

            joinConvoy(truckId: int):boolean

            leaveConvoy(truckId: int):boolean

            accelerateCollectively(truckId: int, speed: float):boolean

            confirmAcceleration(truckId: int, speed: float):boolean

            prepareDeceleration(truckId: int, speed: float):boolean

            decelerateCollectively(truckId: int, speed: float):boolean


        Hint: The respective docstrings hold a detailed behavioural description of the
              service class's functions.
    """

    ###
    # Static properties:
    ###

    # Static private references.
    __maxSpeed__:float = 80.00

    ###
    # Static property functions:
    ###

    @staticmethod
    def setTrucksMaxSpeed(speed: float):
        """[Docstring] Truck's max speed setter."""
        Drive.__maxSpeed__ = speed

    @staticmethod
    def getTrucksMaxSpeed():
        """[Docstring] Truck's max speed getter."""
        return Drive.__maxSpeed__

    ###
    # Truck's driving behaviour:
    ###

    @staticmethod
    def changeSpeed(truckId: int, speed: float):
        """[Docstring] Changes driving speed of a truck.

        Results:

            True        -   In case the truck's new speed could be set.

            False       -   In case the update validation went wrong.

            Exception   -   In case the input validation went wrong.

        Logic:

            Bind truck's object to reference.
            If truck's new speed is inbetween 0 and maxSpeed, set newSpeed as truck's speed.
            If new speed is lower 0, 0 will be as new speed.
            If new speed is above truck's max speed, max speed will be set as new speed.
            Set evaluated newSpeed as truck's speed.
            Save the truck and bind it to a reference.
            Validate update via bound truck object and input.

        """
        truck = Truck.objects.get(truckId=truckId)
        if validate_float(min_value=0, max_value=Drive.getTrucksMaxSpeed(),  value=speed):
            pass
        elif not validate_float(min_value=0, value=speed):
            speed = 0
        elif not validate_float(max_value=Drive.getTrucksMaxSpeed(), value=speed):
            speed = Drive.getTrucksMaxSpeed()
        truck.speed.set(speed)
        val = truck.save(force_insert=True)
        return val.speed == speed
    
    @staticmethod
    def stopTruck(truckId: int):
        """[Docstring] Stopps truck entirely.

        Results:

            True        -   In case the truck's could be stopped.

            False       -   In case the update validation went wrong.

            Exception   -   In case the input validation went wrong.

        Logic:

            Bind truck's object to reference.
            Set new convoy leader's id as truck's respective reference.
            Save the truck and bind it to a reference.
            Validate update via bound truck object and input.

        """
        truck = Truck.objects.get(truckId=truckId)
        truck.speed.set(0)
        val = truck.save(force_insert=True)
        return val.speed == 0

    @staticmethod
    def changeConvoyPosition(truckId: int, newConvoyPosition: int):
        """[Docstring] Changes convoy position reference of a truck.

        Results:

            True        -   In case the truck's convoyPosition reference could be set.

            False       -   In case the update validation went wrong.

            Exception   -   In case the input validation went wrong.

        Logic:

            Bind truck object to reference.
            Set new convoy position as truck's respective reference.
            Save the truck and bind.
            Validate new position in convoy.

        """
        truck = Truck.objects.get(truckId=truckId)
        truck.convoyPosition.set(newConvoyPosition)
        val = truck.save(force=True)
        return val.convoyPosition == newConvoyPosition

    @staticmethod
    def joinConvoy(truckId: int):
        """[Docstring] Join truck to convoy.

        Results:

            True - In case truck has been registered

        Logic:

            Bind truck.
            Form request parameter for api call.
            File request against api.
            Return response code validation.

        """
        truck = Truck.objects.get(truckId=truckId)
        data = {
            'truckId': truck.truckId,
            'address': truck.address
        }
        resp = requests.post(Service.getConvoyAPIAddress(), data=data)
        return resp.status_code == 200

    @staticmethod
    def leaveConvoy(truckId: int):
        """[Docstring] Remove truck from convoy.

        Results:

            True - In case truck has been de-registered

        Logic:

            Bind truck.
            Form request parameter for api call.
            File request against api.
            Return response code validation.

        """
        truck = Truck.objects.get(truckId=truckId)
        data = {
            'truckId': truck.truckId
        }
        resp = requests.delete(Service.getConvoyAPIAddress(), data=data)
        return resp.status_code == 200
    
    @staticmethod
    def accelerateCollectively(truckId: int, speed: float):
        """[Docstring] Makes the whole convoy speed up.

        Results:

            True      - In case truck could accelerate collectively.

            False     - In case any update validation went wrong.

            Exception - In case input validation went wrong.

        Logic:
        
            Bind truck.
            Bind next position.
            Change accelerating status and speed.
            Fetch addresses and then the trucks.
            Sort fetched trucks by their convoy position.
            In case the next trucks exists, make it accelerate aswell.
                Files post api call with repective data.
                data = { 'accelerateCollectively': { 'speed': speed } }
            In case it doesn't, confirm acceleration to previous truck.
                Files post api call with repective data.
                data = { 'confirmAcceleration': { 'speed': speed } }
            Return respective response code validation.

        """
        truck = Truck.objects.get(truckId=truckId)
        position = truck.convoyPosition + 1
        if not Service.changeAccelerationStatus(truckId) or not Drive.changeSpeed(truckId, speed):
            return False
        addresses = Service.fetchTruckAddresses(Service.getConvoyAPIAddress())
        trucks = Service.fetchTrucksInConvoy(addresses)
        trucks = sorted(trucks, key=lambda Truck: Truck.convoyPosition, reverse=False)
        if trucks[position]:
            data = {
                'accelerateCollectively': {
                    'speed': speed
                }
            }
            resp = requests.post(trucks[position].address, data=data)
            return resp.status_code == 200
        else:
            data = {
                'confirmAcceleration': {
                    'speed': speed
                }
            }
            resp = requests.post(trucks[truck.convoyPosition - 1].address, data=data)
            return resp.status_code == 200

    @staticmethod
    def confirmAcceleration(truckId: int, speed: float):
        """[Docstring] Makes the convoy confirm speed up.

        Results:

            True      - In case truck could confirm acceleration.

            False     - In case any update validation went wrong.

            Exception - In case input validation went wrong.

        Logic:
        
            Bind truck.
            Bind previous position.
            Validate speed and change accelerating status.
            Fetch addresses and then the trucks.
            Sort fetched trucks by their convoy position.
            In case the previous trucks exists, confirm acceleration via api call.
                Files post api call with repective data.
                data = { 'confirmAcceleration': { 'speed': speed } }
            Return response code validation.

        """
        truck = Truck.objects.get(truckId=truckId)
        position = truck.convoyPosition - 1
        if truck.speed != speed:
            if not Drive.changeSpeed(truckId, speed):
                return False
        if not Service.changeAccelerationStatus(truckId):
            return False
        addresses = Service.fetchTruckAddresses(Service.getConvoyApiAddress())
        trucks = Service.fetchTrucksInConvoy(addresses)
        trucks = sorted(trucks, key=lambda Truck: Truck.convoyPosition, reverse=False)
        if trucks[position]:
            data = {
                'confirmAcceleration': {
                    'speed': speed
                }
            }
            resp = requests.post(trucks[position].address, data=data)
            return resp.status_code == 200
        else:
            return True
    
    @staticmethod
    def prepareDeceleration(truckId: int, speed: float):
        """[Docstring] Makes the convoy confirm breaking procedure.

        Results:

            True      - In case truck could confirm acceleration.

            False     - In case any update validation went wrong.

            Exception - In case input validation went wrong.

        Logic:
        
            Bind truck.
            Bind next position.
            Change and validate breaking status.
            Fetch addresses and then the trucks.
            Sort fetched trucks by their convoy position.
            In case the next trucks exists, prepare breaking via api call.
                Files post api call with repective data.
                data = { 'prepareDeceleration': { 'speed': speed } }.
            In case the next trucks doesn't exist, confirm breaking to previous truck via api call.
                Files post api call with repective data.
                data = { 'decelerateCollectively': { 'speed': speed } }.
            Return response code validation.

        """
        truck = Truck.objects.get(truckId=truckId)
        position = truck.convoyPosition + 1
        if not Service.changeDecelerationStatus(truckId):
            return False
        addresses = Service.fetchTruckAddresses(Service.getConvoyAPIAddress())
        trucks = Service.fetchTrucksInConvoy(addresses)
        trucks = sorted(trucks, key=lambda Truck: Truck.convoyPosition, reverse=False)
        if trucks[position]:
            data = {
                'prepareDeceleration': {
                    'speed': speed
                }
            }
            resp = requests.post(trucks[position].address, data=data)
            return resp.status_code == 200
        else:
            data = {
                'decelerateCollectively': {
                    'speed': speed
                }
            }
            resp = requests.post(trucks[truck.convoyPosition - 1].address, data=data)
            return resp.status_code == 200

    @staticmethod
    def decelerateCollectively(truckId: int, speed: float):
        """[Docstring] Makes the convoy decelerate collectively.

        Results:

            True      - In case truck could confirm acceleration.

            False     - In case any update validation went wrong.

            Exception - In case input validation went wrong.

        Logic:
        
            Bind truck.
            Bind next position.
            Change and validate breaking status.
            Fetch addresses and then the trucks.
            Sort fetched trucks by their convoy position.
            In case the next trucks exists, prepare breaking via api call.
                Files post api call with repective data.
                data = { 'decelerateCollectively': { 'speed': speed } }.
            Return response code validation.

        """
        truck = Truck.objects.get(truckId=truckId)
        position = truck.convoyPosition + 1
        if not Service.changeDecelerationStatus or not Drive.changeSpeed(truckId, speed):
            return False
        addresses = Service.fetchTruckAddresses(Service.getConvoyAPIAddress())
        trucks = Service.fetchTrucksInConvoy(addresses)
        trucks = sorted(trucks, key=lambda Truck: Truck.convoyPosition, reverse=False)
        if trucks[position]:
            data = {
                'decelerateCollectively': {
                    'speed': speed
                }
            }
            resp = requests.post(trucks[truck.convoyPosition - 1].address, data=data)
            return resp.status_code == 200
        else:
            return True
            
