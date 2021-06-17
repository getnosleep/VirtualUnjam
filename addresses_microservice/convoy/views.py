from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from rest_framework import status
from rest_framework.parsers import JSONParser

import json

class ConvoyViewSet(viewsets.ViewSet):
    registered = {}  # {1: '192.168.0.2:5001'}

    def data(self, request):
        """@return list of adresses of the trucks in this convoy"""
        return JsonResponse(ConvoyViewSet.registered, status=200)
    
    def register(self, request):
        """@return bool success"""
        try:
            data = JSONParser().parse(request)
            truckId = data['truckId']
            address = data['address']
            position = len(ConvoyViewSet.registered) + 1

            ConvoyViewSet.registered[position] = address
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=404)

    # def leave(self, request):
    #     """@return bool success"""
    #     try:
    #         data = JSONParser().parse(request)
    #         truckId = data['truckId']
    #         address = data['address']

    #         if not ConvoyViewSet.__checkEntry__(self, ConvoyViewSet.registered, truckId, address):
    #             raise Exception()

    #         del ConvoyViewSet.registered[truckId]
    #         return HttpResponse(True, status=200)
    #     except:
    #         return HttpResponse(False, status=404)
