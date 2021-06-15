from truck_microservice.truck.properties import MIN_ACCELERATION
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

import json

class ConvoyViewSet(viewsets.ViewSet):
    REGISTERED = {}  # {1: '192.168.0.2:5001'}
    ACCELERATION = {'MIN': -3.5, 'MAX': 2.5}

    def __extractTruckIds__(self):
        """@return truckIds from REGISTERED"""
        keys = ConvoyViewSet.REGISTERED.keys()
        truckIds = []
        for key in keys:
            truckIds.append(key)
        return truckIds

    def __checkEntry__(self, dictionary, key, value):
        """@return success for correct value"""
        if ConvoyViewSet.__checkKey__(self, dictionary, key):
            val = dictionary[key]
            if val == value:
                return True
        return False

    def __checkKey__(self, dictionary, key):
        if key in dictionary.keys():
            return True
        return False

    def data(self, request):
        """@return list of adresses of the trucks in this convoy"""
        return Response(data=ConvoyViewSet.REGISTERED, status=status.HTTP_200_OK)
    
    def truckIds(self, request):
        """@return list of ids of the trucks in this convoy"""
        try:
            truckIds = ConvoyViewSet.__extractTruckIds__(self)
            return Response(data=truckIds, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def address(self, request):
        """@return resolved networkadress for the requested truckId"""
        try:
            data = json.loads(request.body)
            truckId = data['truckId']
            
            if not ConvoyViewSet.__checkKey__(self, ConvoyViewSet.REGISTERED, truckId):
                raise Exception()

            address = ConvoyViewSet.REGISTERED[truckId]
            return Response(data=address, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def register(self, request):
        """@return bool success"""
        try:
            data = json.loads(request.body)
            truckId = data['truckId']
            if ConvoyViewSet.__checkKey__(self, ConvoyViewSet.REGISTERED, key=truckId):
                raise Exception()
            address = data['address']
            ConvoyViewSet.REGISTERED.update({truckId: address})
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def leave(self, request):
        """@return bool success"""
        try:
            data = json.loads(request.body)
            truckId = data['truckId']
            address = data['address']

            if not ConvoyViewSet.__checkEntry__(self, ConvoyViewSet.REGISTERED, truckId, address):
                raise Exception()

            del ConvoyViewSet.REGISTERED[truckId]
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
