from rest_framework import viewsets
from django.http import HttpResponse, JsonResponse

from .models import TruckEntity
from .serializer import ConvoySerializer, AdminSerializer
from .exceptions.initialization import TruckNotInitializedException
from .properties import ID

ERRMSG_UNINITIALIZED = 'Has the truck already been initialized?'

class Query(viewsets.ViewSet):
    def convoyRequests(self, request):
        truck = TruckEntity.objects.get(pk=ID)
        if truck:
            serializer = ConvoySerializer(truck, many=False)
            truckJSON = serializer.data
            return JsonResponse(data=truckJSON, status=200)
        else:
            return HttpResponse(ERRMSG_UNINITIALIZED, status=404)
    
    def adminRequests(self, request):
        truck = TruckEntity.objects.get(pk=ID)
        if truck:
            serializer = AdminSerializer(truck, many=False)
            truckJSON = serializer.data
            return JsonResponse(data=truckJSON, status=200)
        else:
            return HttpResponse(ERRMSG_UNINITIALIZED, status=404)
