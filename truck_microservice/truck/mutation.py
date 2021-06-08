# library imports
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse

# property imports
from .properties import ID, ADDRESS, LENGTH

# persistence layer imports
from .models import TruckEntity
from .serializer import ConvoySerializer, AdminSerializer

# dirty imports
from .intern_services.movement import Movement

# error messages
ERR_MSG_ACCESSABILITY = 'Truck not accessable'

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

    # Just because I'm lazy and don't want to be upset about this fucking program
    def move(self, request):
        pass
