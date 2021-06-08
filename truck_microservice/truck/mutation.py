from django.conf import settings
from rest_framework import serializers, viewsets
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import TruckEntity
from .serializer import Serializer

from .exceptions.initialization import TruckNotInitializedException
from .properties import ID, ADDRESS, LENGTH

class Mutation(viewsets.ViewSet):
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
