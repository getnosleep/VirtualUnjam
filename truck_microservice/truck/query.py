# library importss
from rest_framework import viewsets
from django.http import HttpResponse, JsonResponse

# property imports
from .properties import ID

# persistence layer imports
from .models import TruckEntity
from .serializer import ConvoySerializer, AdminSerializer

# error messages
ERR_MSG_ACCESSABILITY = 'Truck not accessable'

class Query(viewsets.ViewSet):
    def convoyRequests(self, request):
        truck = TruckEntity.objects.get(pk=ID)
        if truck:
            serializer = ConvoySerializer(truck, many=False)
            truckJSON = serializer.data
            return JsonResponse(data=truckJSON, status=200)
        else:
            return HttpResponse(ERR_MSG_ACCESSABILITY, status=404)
    
    def adminRequests(self, request):
        truck = TruckEntity.objects.get(pk=ID)
        if truck:
            serializer = AdminSerializer(truck, many=False)
            truckJSON = serializer.data
            return JsonResponse(data=truckJSON, status=200)
        else:
            return HttpResponse(ERR_MSG_ACCESSABILITY, status=404)
