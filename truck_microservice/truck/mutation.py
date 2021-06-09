# library imports
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse

# property imports
from .properties import ID

# persistence layer imports
from .models import TruckEntity
from .serializer import ConvoySerializer, AdminSerializer

# dirty imports
from .intern_services.movement import movement

# error messages
ERR_MSG_ACCESSABILITY = 'Truck not accessable'

class Mutation(viewsets.ViewSet):
    def joinConvoy(self, request):
        pass

    def leaveConvoy(self, request):
        pass

    def accelerate(self, request):
        success = False
        truck = TruckEntity.objects.get(pk=ID)
        try:
            data = JSONParser().parse(request)
            truck.acceleration = abs(data['acceleration'])
            truck.targetSpeed = data['targetSpeed']
            truck.save()
            # if data['accelerationTime']:
            #     movement.setAccelerationTime(data['accelerationTime'])
            # else:
            #     movement.setAccelerationTime(None)
            success = True
        except:
            pass
        return JsonResponse({'success': success}, status=500)

    def decelerate(self, request):
        success = False
        truck = TruckEntity.objects.get(pk=ID)
        try:
            data = JSONParser().parse(request)
            truck.acceleration = -1 * abs(data['deceleration'])
            truck.targetSpeed = data['targetSpeed']
            truck.save()
            success = True
        except:
            pass
        return JsonResponse({'success': success}, status=500)

    def emergencyBrake(self, request):
        pass

    def poll(self, request):
        pass

    ####  ##### #   #     ##### ####  ##### #   #     ####  ##### #   # ##### #   # ##### #   #
    #   #   #   ##  #     #     #   # #     ##  #     #   # #   # #   # #     #   # #     ##  #
    ####    #   # # #     ##### ####  ##### # # #     ####  ##### #   # #     ##### ##### # # #
    #   #   #   #  ##     #     #   # #     #  ##     #   # #   # #   # #     #   # #     #  ##
    ####  ##### #   #     ##### ####  ##### #   #     #   # #   # ##### ##### #   # ##### #   #
