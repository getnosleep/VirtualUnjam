# library imports
import requests

# property imports
from ..properties import ID, ADDRESS, ADDRESS_MICROSERVICE

"""Convoy requests:"""
def join():
    """@returns bool if successful joined the convoy, else throws exception"""
    data = {'truckId': ID, 'address': ADDRESS}
    resp = requests.post(ADDRESS_MICROSERVICE + '/api', data=data)
    return resp.status_code

def bully(position):
    """@returns bool if successful left the convoy, else throws exception"""
    data = {'truckId': ID, 'address': ADDRESS, 'position': position}
    resp = requests.put(ADDRESS_MICROSERVICE + '/api', data=data)
    return resp.status_code == 200

def registered():
    """@returns dict - {\"truckId\": truckId, \"address\": address} of trucks registered on convoy"""
    return requests.get(ADDRESS_MICROSERVICE + '/api')
