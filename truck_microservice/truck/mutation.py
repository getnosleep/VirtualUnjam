from django.conf import settings
from rest_framework import serializers, viewsets
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import TruckEntity
from .serializer import TruckSerializer

from .exceptions.initialization import TruckNotInitializedException
from .properties import ID, ADDRESS, LENGTH

class Mutation(viewsets.ViewSet):
    def selfInitialize(self, request):
        trucks = TruckEntity.objects.all()
        if trucks.exists():
            TruckEntity.objects.all().delete()
        
        truck = TruckEntity()
        
        truck.save()
        try:
            serializer = TruckSerializer(truck, many=False)
            truckJSON = serializer.data
            return JsonResponse(data=truckJSON, status=200)
        except:
            return HttpResponse('Oh shit, that was an awesome fail...', status=500)

    def joinConvoy(self, request):
        pass

    def leaveConvoy(self, request):
        pass

    def accelerate(self, request):
        pass

    def decelerate(self, request):
        pass

    def emergencyBrake(self, request):
        pass

    def poll(self, request):
        pass
