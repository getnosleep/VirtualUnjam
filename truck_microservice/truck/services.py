import requests # builds up on import urllib3.request
import json
from typing import Final
from rest_framework import status
from .models import Truck
from validation import (
    validate_int, validate_float,
    validate_structure,
    validate_text,
)

"""Properties:"""
__requestType__ = 'http://'
__convoyApiHost__ = '127.0.0.1'
__convoyApiPort__ = 8000
__convoyApiAddress__ = __requestType__ + __convoyAPIHost__ + str(__convoyAPIPort__) 

"""Mutation functionalities and extern property access:"""
def getConvoyApiHost(): return __convoyApiHost__
def setConvoyApiHost(host: str):
    __convoyApiHost__ = host
    pass

def getConvoyApiPort(): return __convoyApiPort__
def setConvoyApiPort(port: int):
    __convoyApiPort__ = port
    pass

def getConvoyApiAddress(): return __convoyApiAddress__
def setConvoyApiAddress(host: str, port: int):
    __convoyApiAddress__ = __requestType__ + host + ':' + str(port)
    pass



def validateTruckObjectStructure(truckId: int):
    """[Docstring] Validates structure of a truck object.
    
    Results:

        True        -   In case the truck's structure could be validated.

        False       -   In case the update validation went wrong.

        Exception   -   In case the input validation went wrong.
    
    Logic:

        Bind truck's object to reference.
        Validate object's structure and serve function call accordingly.

    """
    # Bind truck's object to reference.
    truck = Truck.objects.get(truckId=truckId)
    # Validate object's structure and serve function call accordingly.
    return validate_structure(truck.values(), schema={
                                                        "id": validate_int(min_value = 0),
                                                        "truckId": validate_int(min_value = 0),
                                                        "convoyPosition": validate_int(min_value = 0),
                                                        "convoyLeaderId": validate_int(min_value = 0),
                                                        "speed": validate_float(min_value = 0, max_value = Drive.getMaxSpeed()),
                                                        "address": validate_text(min_length=8),
                                                        "isBroken": validate_int(min_value=0, max_value=1),
                                                        "isProlling": validate_int(min_value=0, max_value=1),
                                                        "isAccelerating": validate_int(min_value=0, max_value=1),
                                                        "isDecelerating": validate_int(min_value=0, max_value=1)
                                                    })

"""
# Sehr gute Idee, allerdings gehoert das in jedem Falle, egal wie man es macht in das Truck Objekt, da es eine interne Validierung ist (auch bei models.Model())
# Siehe Truck.isLeader()


@staticmethod
def validateConvoyLeadership(truckId: int):
    [Docstring] Validates convoy leadership of a truck object.
    
    Results:

        True        -   In case the truck object is its' convoy's leader.

        False       -   In case the update validation went wrong.

        Exception   -   In case the input validation went wrong.

    Logic:

        Bind truck's object to reference.
        Validate if truck is the leader of its' convoy and serve function call accordingly.

    
    truck = Truck.objects.get(truckId=truckId)
    return truck.truckId == truck.convoyLeaderId
"""






def fetchTruckAddresses(address: str):
    """
        @returns dictionary of truck addresses in the convoy
        @throws service not available
    """
    response = requests.get(__requestType__ + address)

    if response.status_code == status.HTTP_200_OK:
        return json.load(response)
    raise('Bad Request')

def fetchTrucksInConvoy(addresses: dict):
    """[Docstring] Fetches convoy's trucks.

    Results:

        True        -   In case the truck could be fetched.

        False       -   In case the update validation went wrong.

        Exception   -   In case the input validation went wrong.

    Logic:

        Iterates trucks.
        In case truck is behind, removes it from list.
        Returns trucks in front.
    """
    trucks = set([Truck])
    for address in addresses.values():
        truckJson = requests.get('http://' + address)
        if truckJson.status_code == status.HTTP_200_OK:
            truckDict = json.load(truckJson)
            trucks.add(Truck(truckId=truckDict['truckId'],
                                convoyPosition=truckDict['convoyPosition'],
                                convoyLeaderId=truckDict['convoyLeaderId'],
                                speed=truckDict['speed'],
                                isBroken=truckDict['isBroken'],
                                isPolling=truckDict['isPolling'],
                                address=address
                                )
                        )
        else:
            raise('Bad Request')
    return trucks

def determineRelevantTrucksInConvoy(position: int, trucks: set([Truck])):
    """[Docstring] Determines trucks in front.

    Results:

        Set([Truck]) -   Set with trucks in front.

        Exception    -   In case the input validation went wrong.

    Logic:

        Iterates trucks.
        In case truck is behind, removes it from list.
        Returns trucks in front.
    """
    for convoyTruck in trucks:
        if convoyTruck.convoyPosition >= position or convoyTruck.isBroken():
            trucks.discard(convoyTruck)
        else:
            pass
    return trucks

def repairTruck():
    if Truck.isBroken():
        Truck.toggleBroken()

def destroyTruck():
    if not Truck.isBroken():
        Truck.toggleBroken()
