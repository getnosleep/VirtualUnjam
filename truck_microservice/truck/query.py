# library importss
from rest_framework import viewsets
from django.http import HttpResponse, JsonResponse

# property imports
from .properties import ID

# persistence layer imports
from .models import TruckEntity
from .serializer import BullySerializer, ConvoySerializer, AdminSerializer

# error messages
ERR_MSG_ACCESSABILITY = 'Truck not accessable'

class Query(viewsets.ViewSet):
    def truckRequests(self, request):
        """"@returns everything a truck needs to identify the truck in front or behind it"""
        truck = TruckEntity.objects.get(pk=ID)
        if truck:
            serializer = ConvoySerializer(truck, many=False)
            truckJSON = serializer.data
            return JsonResponse(data=truckJSON, status=200)
        else:
            return HttpResponse(ERR_MSG_ACCESSABILITY, status=404)
    
    def adminRequests(self, request):
        """@returns a sertialized Truck with specific information for the Homepage => just used for Postman to see, what the truck would look like"""
        truck = TruckEntity.objects.get(pk=ID)
        if truck:
            serializer = AdminSerializer(truck, many=False)
            truckJSON = serializer.data
            return JsonResponse(data=truckJSON, status=200)
        else:
            return HttpResponse(ERR_MSG_ACCESSABILITY, status=404)
    
    def pollRequests(self, request):
        """@returns a serialized Truck with specific information for bullying"""
        truck = TruckEntity.objects.get(pk=ID)
        if truck:
            serializer = BullySerializer(truck, many=False)
            truckJSON = serializer.data
            return JsonResponse(data=truckJSON, status=200)
        else:
            return HttpResponse(ERR_MSG_ACCESSABILITY, status=404)
