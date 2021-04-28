"""[Docstring] Declares functions altering trucks' properties."""
import requests # builds up on import urllib3.request
import json
from typing import Final
from rest_framework import status
from .drive import Drive
from .models import Truck
from validation import (
    validate_int, validate_float,
    validate_structure,
    validate_text,
)

class Service(object):
    """[Docstring] Declares functions altering trucks' properties.
    
    Properties:
        
        convoyAPIHost:   private static string
        
        convoyAPIPort:   private static int

        convoyAPIAddress: private static string
    
    Functions: 

        Names, inputs and results:

            Static porperties' functions:

                setConvoyApiHost(host: str):

                getConvoyApiHost():str

                setConvoyApiPort(port: int):

                getConvoyApiPort():int

                setConvoyApiAddress(host: str, port: int):
                
                getConvoyApiAddress():str

            Validation functions:

                validateTruckObjectStructure(truckId):boolean

                validateConvoyLeadership(truckId):boolean

            Truck's api behaviour:

                fetchTruckAddresses(address: str):set

                fetchTrucksInConvoy(addresses: dict):set

                determineRelevantTrucksInConvoy(position: int, trucks: set([Truck])):set
            
                adjustSpeedToTruck(truckId, idolTruckId):boolean
            
                stopTruck(truckId):boolean

                changeConvoyPosition(truckId, newConvoyPosition):boolean
            
            Modeling functions:
                
                repairTruck(truckId: int):boolean

                destroyTruck(truckId: int):boolean

                changeTruckIdentificator(truckId: int, newTruckId: int):boolean
            
                changeConvoyLeader(truckId: int, leaderId: int):boolean

                changePollingStatus(truckId: int):boolean

                changeDecelerationStatus(truckId: int):boolean

                changeAccelerationStatus(truckId: int):boolean

        Hint: The respective docstrings hold a detailed behavioural description of the
              service class's functions.
    """
    
    ###
    # Static properties:
    ###

    # Static private references.
    __convoyAPIHost__:str = '127.0.0.1'
    __convoyAPIPort__:str = 8000
    __convoyAPIAddress__:str = 'http://127.0.0.1:8000'

    ###
    # Static property functions:
    ###

    @staticmethod
    def setConvoyApiHost(host: str):
        """[Docstring] Convoy host setter."""
        Service.__convoyAPIHost__ = host

    @staticmethod
    def getConvoyApiHost():
        """[Docstring] Convoy host getter."""
        return Service.__convoyAPIHost__
    
    @staticmethod
    def setConvoyApiPort(port: int):
        """[Docstring] Convoy port setter."""
        Service.__convoyAPIPort__ = port
    
    @staticmethod
    def getConvoyApiPort():
        """[Docstring] Convoy port getter."""
        return Service.__convoyAPIPort__
    
    @staticmethod
    def setConvoyApiAddress(host: str, port: int):
        """[Docstring] Convoy address setter."""
        Service.__convoyAPIPort__ = 'http://' + host + ':' + str(port)

    @staticmethod
    def getConvoyApiAddress():
        """[Docstring] Convoy address getter."""
        return Service.__convoyAPIAddress__

    ###
    # Validation functions:
    ###

    @staticmethod
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
                                                          "speed": validate_float(min_value = 0, max_value = Drive.maxSpeed),
                                                          "address": validate_text(min_length=8)
                                                        })

    @staticmethod
    def validateConvoyLeadership(truckId: int):
        """[Docstring] Validates convoy leadership of a truck object.
        
        Results:

            True        -   In case the truck object is its' convoy's leader.

            False       -   In case the update validation went wrong.

            Exception   -   In case the input validation went wrong.

        Logic:

            Bind truck's object to reference.
            Validate if truck is the leader of its' convoy and serve function call accordingly.

        """
        truck = Truck.objects.get(truckId=truckId)
        return truck.truckId == truck.convoyLeaderId

    ###
    # Api calls:
    ###

    @staticmethod
    def fetchTruckAddresses(address: str):
        """[Docstring] Fetches convoy truck's addresses.

        Results:

            Dict        -   In case the addresses could be fetched.

            Exception   -   In case the input validation went wrong.

        Logic:

            Iterates trucks.
            In case truck is behind, removes it from list.
        """
        addressesJson = requests.get('http://' + address)

        if addressesJson.status_code == status.HTTP_200_OK:
            addresses = json.load(addressesJson)
        else:
            raise('Bad Request')

        return addresses

    @staticmethod
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
        for id, address in addresses.items():
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

    @staticmethod
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
    
    ###
    # Truck's modelling functions:
    ###

    @staticmethod
    def repairTruck(truckId: int):
        """[Docstring] Changes isBroken reference on a truck to false.

        Results:

            True        -   In case the truck is repaired.

            False       -   In case the update validation went wrong.

            Exception   -   In case the input validation went wrong.

        Logic:

            Bind truck's object to reference.
            Set new truckId as truck's respective reference.
            Save the truck and bind it to a reference.
            Validate update via bound truck object and input.
        """
        truck = Truck.objects.get(truckId=truckId)
        truck.isBroken.set(False)
        val = truck.save(force_insert=True)
        return val.isBroken == False

    @staticmethod
    def destroyTruck(truckId: int):
        """[Docstring] Changes isBroken reference on a truck to true.

        Results:

            True        -   In case the truck is destroyed.

            False       -   In case the update validation went wrong.

            Exception   -   In case the input validation went wrong.

        Logic:

            Bind truck's object to reference.
            Set new truckId as truck's respective reference.
            Save the truck and bind it to a reference.
            Validate update via bound truck object and input.
        """
        truck = Truck.objects.get(truckId=truckId)
        truck.isBroken.set(True)
        val = truck.save(force_insert=True)
        return val.isBroken == True
    
    @staticmethod
    def changeTruckIdentificator(truckId: int, newTruckId: int):
        """[Docstring] Changes identificator of a truck.
        
        Results:

            True        -   In case the truck's truckId reference could be set.

            False       -   In case the update validation went wrong.

            Exception   -   In case the input validation went wrong.

        Logic:

            Bind truck's object to reference.
            Set new value.
            Save the truck and bind it to a reference.
            Validate update via bound truck object and input.
        """
        truck = Truck.objects.get(truckId=truckId)
        truck.truckId.set(newTruckId)
        val = truck.save(force_insert=True)
        return val.truckId == newTruckId

    @staticmethod
    def changeConvoyLeader(truckId: int, leaderId: int):
        """[Docstring] Change convoy's leader reference of a truck.

        Results:

            True        -   In case the truck's convoyLeaderId reference could be set.

            False       -   In case the update validation went wrong.

            Exception   -   In case the input validation went wrong.

        Logic:

            Bind truck object to reference.
            Set new convoy leader's id as truck's respective reference.
            Save the truck and bind it to a reference.
            Validate update via bound truck object and input.

        """
        truck = Truck.objects.get(truckId=truckId)
        truck.convoyLeaderId.set(leaderId)
        val = truck.save(force_insert = True)
        return val.convoyLeaderId == leaderId

    @staticmethod
    def changePollingStatus(truckId: int):
        """[Docstring] Change convoy's leader reference of a truck.

        Results:

            True        -   In case the truck's convoyLeaderId reference could be set.

            False       -   In case the update validation went wrong.

            Exception   -   In case the input validation went wrong.

        Logic:

            Bind truck object to reference.
            Bind validation value to reference
            Set new convoy leader's id as truck's respective reference.
            Save the truck and bind it to a reference.
            Validate update via bound truck object and input.

        """
        truck = Truck.objects.get(truckId=truckId)
        valAtt = truck.isPolling 
        truck.isPolling.set(not truck.isPolling)
        val = truck.save(force_insert=True)
        return val.isPolling != valAtt

    @staticmethod
    def changeDecelerationStatus(truckId: int):
        """[Docstring] Changes deceleration status of a truck.

        Results:

            True        -   In case the truck's breaking status could be changed.

            False       -   In case the update validation went wrong.

            Exception   -   In case the input validation went wrong.

        Logic:

            Bind truck object to reference.
            Bind validation value to reference
            Set new value.
            Save the truck and bind it to a reference.
            Validate update via bound truck object and input.

        """
        truck = Truck.objects.get(truckId=truckId)
        valAtt = truck.isDecelerating
        truck.isDecelerating.set(not truck.isDecelerating)
        val = truck.save(force_insert=True)
        return val.isDecelerating != valAtt

    @staticmethod
    def changeAccelerationStatus(truckId: int):
        """[Docstring] Change accelerating status of a truck.

        Results:

            True        -   In case the truck's acceleration status could be changed.

            False       -   In case the update validation went wrong.

            Exception   -   In case the input validation went wrong.

        Logic:

            Bind truck object to reference.
            Bind validation value to reference
            Set new value.
            Save the truck and bind it to a reference.
            Validate update via bound truck object and input.

        """
        truck = Truck.objects.get(truckId=truckId)
        valAtt = truck.isAccelerating
        truck.isAccelerating.set(not truck.isAccelerating)
        val = truck.save(force_insert=True)
        return val.isAccelerating != valAtt
