from rest_framework import viewsets
from rest_framework import permissions
from . import serializers
from . import models

# Trucks view set class.
class TruckViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None): # /api/truck/<str:id>
        """
        return:
            id
            speed
            length
            distance
            optimal_distance
        """
        pass
    
    def update_fleet(self, request, pk=None):
        """
        model.fleet = request.fleet
        """
        pass

    def set_speed(self, request, pk=None): # /api/truck/<str:id>
        """
        model.speed = request.speed

        return:
            id
            speed
            length
            distance
            optimal_distance
        """
        pass

    def alive(self, request, pk=None):
        return True
