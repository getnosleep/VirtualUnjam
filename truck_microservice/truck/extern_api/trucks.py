# library imports
import requests

# property imports
from ..properties import ID, ADDRESS

"""Intern convoy requests:"""
def convoyRequest(address):
    """@returns the status of the requested truck"""
    data = {'truckId': ID, 'address': ADDRESS}
    return requests.delete(address + '/api/convoy', data=data)
