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

"""Convoy functionalities:"""
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
