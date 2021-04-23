from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

import json

REGISTERED = {} # {1: '192.168.0.2:5001'}

def __extractTruckIds__():
    """@return truckIds from REGISTERED"""
    keys = REGISTERED.keys()
    truckIds = []
    for key in keys:
        truckIds.append(key)
    return truckIds

def __checkEntry__(dictionary, key, value):
    """@return success for correct value"""
    if __checkKey__(dictionary, key):
        val = dictionary[key]
        if val == value:
            return True
    return False

def __checkKey__(dictionary, key):
    if key in dictionary.keys():
        val = dictionary[key]
        return True
    return False

class ConvoyViewSet(viewsets.ViewSet):
    def data(self, request):
        """@return list of adresses of the trucks in this convoy"""
        return Response(data=REGISTERED, status=status.HTTP_200_OK)
    
    def truckIds(self, request):
        """@return list of ids of the trucks in this convoy"""
        try:
            truckIds = __extractTruckIds__()
            return Response(data=truckIds, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def address(self, request):
        """@return resolved networkadress for the requested truckId"""
        try:
            data = json.loads(request.body)
            truckId = data['truckId']
            
            if not __checkKey__(REGISTERED, truckId):
                raise Exception()

            address = REGISTERED[truckId]
            return Response(data=address, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def register(self, request):
        """@return bool success"""
        try:
            data = json.loads(request.body)
            truckId = data['truckId']
    	    if __checkKey__(REGISTERED, truckId):
                raise Exception()
            address = data['address']
            REGISTERED.update({truckId: address})
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def leave(self, request):
        """@return bool success"""
        try:
            data = json.loads(request.body)
            truckId = data['truckId']
            address = data['address']

            if not __checkEntry__(REGISTERED, truckId, address):
                raise Exception()

            del REGISTERED[truckId]
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
