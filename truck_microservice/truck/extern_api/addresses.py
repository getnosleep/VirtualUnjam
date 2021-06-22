# library imports
import requests
import json
from requests.exceptions import Timeout

# property imports
from ..properties import ID, ADDRESS_SELF, ADDRESS_CONVOY, MAX_TIMEOUT

"""Convoy requests:"""
def join():
    """@returns bool if successful joined the convoy, else throws exception"""
    try:
        data = {'address': ADDRESS_SELF}
        headers = {'content-type': 'application/json'}
        return requests.post('http://' + ADDRESS_CONVOY + '/api/', data=json.dumps(data), headers=headers, timeout=MAX_TIMEOUT)
    except Timeout as t:
        return False

def registered():
    """@returns dict - {\"truckId\": truckId, \"address\": address} of trucks registered on convoy"""
    try:
        return requests.get('http://' + ADDRESS_CONVOY + '/api/', timeout=MAX_TIMEOUT)
    except Timeout as t:
        return False

def overwriteRegistration(oldPosition, newPosition):
    """@returns the status of the requested truck"""
    try:
        data = {
            'oldPosition': oldPosition,
            'newPosition': newPosition,
            'address': ADDRESS_SELF
        }
        headers = {'content-type': 'application/json'}
        return requests.put('http://' + ADDRESS_CONVOY + '/api/', data=json.dumps(data), headers=headers, timeout=MAX_TIMEOUT)
    except Timeout as t:
        return False
