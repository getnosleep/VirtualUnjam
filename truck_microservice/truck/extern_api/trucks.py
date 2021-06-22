# library imports
import requests
import json
from requests.exceptions import Timeout

# property imports
from ..properties import ID, ADDRESS_SELF, MAX_TIMEOUT

"""Intern convoy requests:"""

# get:truck
def convoyRequest(address):
    try:
        # Naja, hier muss man nochmal was machen
        # data = {'truckId': ID, 'address': ADDRESS_SELF}
        # headers = {'content-type': 'application/json'}
        return requests.get('http://' + address + '/api/truck', timeout=MAX_TIMEOUT)#data=json.dumps(data), headers=headers, timeout=MAX_TIMEOUT)
    except Timeout:
        return False

# get:poll
def pollRequest(address):
    try:
        return requests.get('http://' + address + '/api/poll', timeout=MAX_TIMEOUT)
    except Timeout:
        return False

# post:leader
# def greetAsLeader(address):
#     try:
#         data = {
#             'leader': ADDRESS_SELF,
#         }
#         headers = {'content-type': 'application/json'}
#         return requests.post('http://' + address + '/api/leader', data=json.dumps(data), headers=headers, timeout=MAX_TIMEOUT)
#     except Timeout:
#         return False

# put:convoy
def joinBehind(address):
    try:
        data = {
            'backTruckAddress': ADDRESS_SELF,
        }
        headers = {'content-type': 'application/json'}
        return requests.put('http://' + address + '/api/convoy', data=json.dumps(data), headers=headers, timeout=MAX_TIMEOUT)
    except Timeout:
        return False

# post:intact
def crashTruck(address):
    try:
        return requests.delete('http://' + address + '/api/intact', timeout=MAX_TIMEOUT)
    except Timeout:
        return False

# post:accelerate
def accelerate(address, targetSpeed, acceleration, heartbeatTick):
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

# post:bully
def startBullying(address):
    try:
        data = {
            'backTruckAddress': ADDRESS_SELF,
        }
        headers = {'content-type': 'application/json'}
        return requests.post('http://' + address + '/api/bully', data=json.dumps(data), headers=headers, timeout=MAX_TIMEOUT)
    except Timeout:
        return False

# put:bully
def bullyAcknowledgement(address, leader, position):
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
