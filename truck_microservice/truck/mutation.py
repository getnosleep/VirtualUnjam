from django.conf import settings
from rest_framework import serializers, viewsets
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import TruckEntity
from .serializer import TruckSerializer

from .exceptions.initialization import TruckNotInitializedException
from .initializer import TRUCK_ID

class Mutation(viewsets.ViewSet):
    def view(self, request):
        pass
