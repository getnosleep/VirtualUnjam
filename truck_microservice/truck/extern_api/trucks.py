# library imports
import requests

# property imports
from ..properties import ID, ADDRESS

"""Intern convoy requests:"""
def convoyRequest(address):
    """@returns the status of the requested truck"""
    data = {'truckId': ID, 'address': ADDRESS}
    return requests.delete('http://' + address + '/api/convoy', data=data)

    # Hier muessen noch die Mutations mit bei, wie bspw. Ich bin neuer Truck hinter dir, oder Ich leave den Convoy vor dir oder ich bin Fuehrer. Akzeptier das oder geh kaputt...
