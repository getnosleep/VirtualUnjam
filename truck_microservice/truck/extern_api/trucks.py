# library imports
import requests
import json
from requests.exceptions import Timeout

# property imports
from ..properties import ID, ADDRESS_SELF, MAX_TIMEOUT

"""Intern convoy requests:"""
def convoyRequest(address):
    """@returns the status of the requested truck"""
    try:
        # Naja, hier muss man nochmal was machen
        data = {'truckId': ID, 'address': ADDRESS_SELF}
        headers = {'content-type': 'application/json'}
        return requests.post('http://' + address + '/api/truck', data=json.dumps(data), headers=headers, timeout=MAX_TIMEOUT)
    except Timeout:
        return False

def pollRequest(address):
    """@returns the status of the requested truck"""
    try:
        return requests.get('http://' + address + '/api/poll', timeout=MAX_TIMEOUT)
    except Timeout:
        return False

def accelerate(address, targetSpeed, acceleration, heartbeatTick):
    """@returns the status of the requested truck"""
    try:
        data = {
            'targetSpeed': targetSpeed,
            'acceleration': acceleration,
            'heartbeatTick': heartbeatTick,
        }
        headers = {'content-type': 'application/json'}
        return requests.post('http://' + address + '/api/accelerate', data=json.dumps(data), headers=headers, timeout=MAX_TIMEOUT)
    except Timeout:
        return False

def bullyAcknowledgement(address, leader, position):
    """@returns the status of the requested truck"""
    try:
        data = {
            'newLeader': leader,
            'frontTruckAddress': ADDRESS_SELF,
            'frontTruckPosition': position,
        }
        headers = {'content-type': 'application/json'}
        return requests.put('http://' + address + '/api/bully', data=json.dumps(data), headers=headers, timeout=MAX_TIMEOUT)
    except Timeout:
        return False

def startBullying(address):
    """@returns the status of the requested truck"""
    try:
        data = {
            'backTruckAddress': ADDRESS_SELF,
        }
        headers = {'content-type': 'application/json'}
        return requests.post('http://' + address + '/api/bully', data=json.dumps(data), headers=headers, timeout=MAX_TIMEOUT)
    except Timeout:
        return False

    # Hier muessen noch die Mutations mit bei, wie bspw. Ich bin neuer Truck hinter dir, oder Ich leave den Convoy vor dir oder ich bin Fuehrer. Akzeptier das oder geh kaputt...
