from rest_framework import viewsets
from rest_framework import permissions
from . import serializers
from . import models

# Trucks view set class.
class TruckBehaviour(viewsets.ViewSet):
    def alive(self, request, pk=None):
        return True

    def accelerate(self, request, pk=None):
        pass

    def decelerate(self, request, pk=None):
        pass

    def stop(self, request, pk=None):
        pass
    
    def joinConvoy(self, request, pk=None):
        pass

    def leaveConvoy(self, request, pk=None):
        pass

class TruckMonitoring(viewsets.ViewSet):
    def retrieve(self, request, pk=None): # monitoring interface - host:port/truck/<str:id>
        """
        return:
            id
            speed
            length
            distance
            optimal_distance
        """
        pass



    #def speed_monitor ... etc -> because of CQRS
