import requests

"""Properties:"""
__requestType__ = 'http://'
__convoyApiHost__ = '127.0.0.1'
__convoyApiPort__ = 8000
__convoyApiAddress__ = __requestType__ + __convoyApiHost__ + str(__convoyApiPort__)

"""Extern property access:"""
def getConvoyApiHost(): return __convoyApiHost__
def getConvoyApiPort(): return __convoyApiPort__
def getConvoyApiAddress(): return __convoyApiAddress__

"""Convoy requests:"""
def join(truckId, address):
    """@returns bool - successful joined the convoy"""
    data = {'truckId': truckId, 'address': address}
    resp = requests.post(__convoyApiAddress__, data=data)
    return resp.status_code == 200

def leave(truckId):
    """@returns bool - successful left the convoy"""
    data = {'truckId': truckId}
    resp = requests.delete(__convoyApiAddress__, data=data)
    return resp.status_code == 200

def registered():
    """@returns dict - {\"truckId\": truckId, \"address\": address} of trucks registered on convoy"""
    pass
