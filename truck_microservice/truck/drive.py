"""[Docstring] Service class handling truck's driving behaviour."""
import requests
from typing import Final
from rest_framework import status
from .services import *
from .models import Truck
from validation import (
    validate_int, validate_float,
    validate_structure,
    validate_text,
)

"""Properties:"""
__minSpeed__ = 0.0
__maxSpeed__ = 80.0

"""Extern property access:"""
def getMinSpeed(): return __minSpeed__
def getTrucksMaxSpeed(): return __maxSpeed__

"""Mutation functionalities:"""
def changeSpeed(speed: float):
    """
        @returns the speed that has been set to the truck
        @raise input validation error
    """
    if validate_float(min_value=__minSpeed__, max_value=__maxSpeed__, value=speed):
        pass
    elif speed > __maxSpeed__:
        speed = __maxSpeed__
    else:
        speed = __minSpeed__
    Truck.setSpeed(speed=speed)
    return speed

def stopTruck():
    changeSpeed(__minSpeed__)

def changeConvoyPosition(newConvoyPosition: int):
    Truck.setConvoyPosition(newConvoyPosition)

def accelerateCollectively(speed: float):
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
    position = Truck.getConvoyPosition() + 1
    uri = getConvoyApiAddress()

    if not Truck.isAccelerating():
        Truck.toggleAccelerating()
    
    changeSpeed(speed=speed)
    
    addresses = fetchTruckAddresses(uri)
    truckReferences = fetchTrucksInConvoy(addresses)

    # Okay, ich gebe zu... ich habe mich ein wenig unklar ausgedrueckt xD

    truckReferences = sorted(truckReferences, key=lambda Truck: Truck.convoyPosition, reverse=False)
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
