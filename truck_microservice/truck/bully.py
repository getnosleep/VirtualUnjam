"""[Docstring] Declares electoral functions, determining the new convoy leader."""
import requests
import json
from typing import Final
from rest_framework import status
from .convoy import *
from .services import *
from .drive import *
from .models import Truck
from validation import (
    validate_int, validate_float,
    validate_structure,
    validate_text,
)

class Bully:
    """[Docstring] Declares electoral functions, determining the new convoy leader.
    
    Functions: 

        Names, inputs and results:

            Bullying functions:

                startPolling(truckId):boolean

                bullyRelevantTrucks(truckIds):list

        Hint: The respective docstrings hold a detailed behavioural description of the
              service class's functions.
    """

    @staticmethod
    def startPolling(truckId: int):
        """[Docstring] Starts polling procedure among truck and trucks in front.

        Results:

            True        -   In case the polling process change truck's convoy position.

            False       -   In case the update validation went wrong.

            Exception   -   In case the input validation went wrong.

        Logic:
    
            Bind truck.
            In case truck is polling, stop.
            Change and validate truck's polling status.
            Fetch and validate addresses and trucks.
            Determine relevant trucks.
            Bully relevant trucks.
            In case new position is leader, signal leadership convoy's trucks.
            Change truck's convoy position.
            Return position change validation.

        """
        truck = Truck.objects.get(truckId=truckId)
        if truck.isPolling or not Service.changePollingStatus(truck.truckId):
            return False
        addresses = Service.fetchTruckAddresses(Service.getConvoyAPIAddress())
        trucksInConvoy = Service.fetchTrucksInConvoy(addresses)
        relevantTrucksInConvoy = Service.determineRelevantTrucksInConvoy(truck.convoyPosituion, trucksInConvoy)
        Bully.bullyRelevantTrucks(relevantTrucksInConvoy)
        newPosition = len(relevantTrucksInConvoy)
        if newPosition == 0:
            Bully.signalConvoyLeadership(truck.truckId, addresses)
            Service.changeConvoyLeader(truckId, truckId)
        return Drive.changeConvoyPosition(truckId, newPosition)

    @staticmethod
    def bullyRelevantTrucks(trucks: set([Truck])):
        """[Docstring] Tells other trucks in convoy to start polling.

        Results:

            True        -   In case the trucks could be bullied.

            False       -   In case the api call went wrong.

            Exception   -   In case the input validation went wrong.

        Logic:

            Bind error flag.
            Iterate trucks.
            If iterated truck is not polling, make it via api call.
            Validate response code via error flag reference.
            Return error flag.

        """
        flag = True
        for convoyTruck in trucks:
            if not convoyTruck.isPolling:
                resp = requests.head('http://' + trucks.address)
                if resp.status_code != 200:
                    flag = False
        return flag

    @staticmethod
    def signalConvoyLeadership(truckId: int, addresses: dict):
        """[Docstring] Tells other trucks to accept truck as leader.

        Results:

            True        -   In case the leader could be signal.

            False       -   In case the api call went wrong.

            Exception   -   In case the input validation went wrong.

        Logic:

            Bind error flag.
            Iterate addressess.
            Signal leadership for each address.
            Validate response code via error flag reference.
            Return error flag.

        """
        flag = True
        for id, address in addresses.items():
            data = {
                'leadership': {
                    'leaderId': truckId
                }
            }
            resp = requests.post(address, data=data)
            if resp.status_code != 200:
                flag = False
        return flag
