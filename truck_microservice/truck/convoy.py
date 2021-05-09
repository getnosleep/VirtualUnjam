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

def joinConvoy():
    """
        @returns bool - successful joined the convoy
    """
    data = {'truckId': Truck.getTruckId(), 'address': Truck.getAddress()}
    uri = Service.getConvoyAPIAddress()
    resp = requests.post(uri, data=data)
    return resp.status_code == 200

def leaveConvoy():
    """
        @returns bool - successful left the convoy
    """
    data = {'truckId': Truck.getTruckId}
    resp = requests.delete(Service.getConvoyAPIAddress(), data=data)
    if resp.status_code == 200:
        Truck.setIndependent()
        return True
    return False
