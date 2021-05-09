import requests
from .models import Truck

"""Properties:"""
__requestType__ = 'http://'
__convoyApiHost__ = '127.0.0.1'
__convoyApiPort__ = 8000
__convoyApiAddress__ = __requestType__ + __convoyApiHost__ + str(__convoyApiPort__)

"""Extern property access:"""
def getConvoyApiHost(): return __convoyApiHost__
def getConvoyApiPort(): return __convoyApiPort__
def getConvoyApiAddress(): return __convoyApiAddress__

"""Convoy functionalities:"""
def joinConvoy():
    """@returns bool - successful joined the convoy"""
    data = {'truckId': Truck.getTruckId(), 'address': Truck.getAddress()}
    resp = requests.post(__convoyApiAddress__, data=data)
    return resp.status_code == 200

def leaveConvoy():
    """@returns bool - successful left the convoy"""
    data = {'truckId': Truck.getTruckId}
    resp = requests.delete(__convoyApiAddress__, data=data)
    if resp.status_code == 200:
        Truck.setIndependent()
        return True
    return False
