# library imports
import requests

# property imports
from ..properties import ID, ADDRESS_SELF, ADDRESS_CONVOY

SERVER = 'http://' + ADDRESS_CONVOY + '/api/'

"""Convoy requests:"""
def join():
    """@returns bool if successful joined the convoy, else throws exception"""
    data = {'truckId': ID, 'address': ADDRESS_SELF}
    resp = requests.post(SERVER, data=data)
    return resp.status_code

def bully(position):
    """@returns bool if successful left the convoy, else throws exception"""
    data = {'truckId': ID, 'address': ADDRESS_SELF, 'position': position}
    resp = requests.put(SERVER, data=data)
    return resp.status_code == 200

def registered():
    """@returns dict - {\"truckId\": truckId, \"address\": address} of trucks registered on convoy"""
    return requests.get(SERVER)
