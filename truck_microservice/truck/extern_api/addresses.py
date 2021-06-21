# library imports
import requests
from requests.exceptions import Timeout

# property imports
from ..properties import ID, ADDRESS_SELF, ADDRESS_CONVOY, MAX_TIMEOUT

SERVER = 'http://' + ADDRESS_CONVOY + '/api/'

"""Convoy requests:"""
def join():
    """@returns bool if successful joined the convoy, else throws exception"""
    data = {'truckId': ID, 'address': ADDRESS_SELF}
    resp = requests.post(SERVER, data=data)
    return resp.status_code

def registered():
    """@returns dict - {\"truckId\": truckId, \"address\": address} of trucks registered on convoy"""
    return requests.get(SERVER)

def overwriteRegistration(oldPosition, newPosition):
    """@returns the status of the requested truck"""
    try:
        data = {
            'oldPosition': oldPosition,
            'newPosition': newPosition,
            'address': ADDRESS_SELF
        }
        return requests.put('http://' + ADDRESS_CONVOY + '/api/poll', data=data, timeout=MAX_TIMEOUT)
    except Timeout:
        return False