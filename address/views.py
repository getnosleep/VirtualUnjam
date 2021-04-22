from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

import json

REGISTERED = {} # {1: '192.168.0.2:5001'}

class ConvoyViewSet(viewsets.ViewSet):
    """
    def create(self, request):
        convoy = request.convoy
        try:
            serializer = ConvoySerializer(data=convoy)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(data=convoy, status=status.HTTP_406_NOT_ACCEPTABLE)
    """

    def data(self, request):
        """@return list of adresses of the trucks in this convoy"""
        return Response(data=REGISTERED, status=status.HTTP_200_OK)
    
    def truckIds(self, request):
        """@return list of ids of the trucks in this convoy"""
        truckIds = []
        return Response(data=truckIds, status=status.HTTP_200_OK)
    
    def address(self, request, truckId: int):
        """@return resolved networkadress for the requested truckId"""
        try:
            address = ''
            return Response(data=address, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def register(self, request):
        """@return bool success"""
        try:
            data = json.loads(request.body)
            truckId = data['truckId']
            address = data['address']
            REGISTERED.update({truckId: address})
            return Response(data=REGISTERED, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        """
        try:
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        """

    def leave(self, request, truckId: int):
        """@return bool success"""
        try:
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
