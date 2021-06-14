# library imports
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse

# property imports
from .properties import ID, MIN_SPEED, MIN_ACCELERATION

# persistence layer imports
from .models import TruckEntity

# dirty imports
from .daemons import movement

# extern requests
from .extern_api import convoy

# error messages
ERR_MSG_ACCESSABILITY = 'Truck not accessible'
ERR_MSG_JOIN = 'Joining the convoy wasn\'t possible for unknown reason'
ERR_MSG_LEAVE = 'Leaving the convoy wasn\'t possible for unknown reason'

class Mutation(viewsets.ViewSet):
    def joinConvoy(self, request):
        try:
            status = convoy.join()
            HttpResponse(status=status)
        except:
            HttpResponse(ERR_MSG_JOIN, status=500)

    def leaveConvoy(self, request):
        try:
            status = convoy.leave()
            HttpResponse(status=status)
        except:
            HttpResponse(ERR_MSG_LEAVE, status=500)

    def accelerate(self, request):
        success = False
        truck = TruckEntity.objects.get(pk=ID)
        try:
            data = JSONParser().parse(request)
            truck.acceleration = abs(data['acceleration'])
            truck.targetSpeed = data['targetSpeed']
            
            # => sollte eingesetzt werden, sobald der Broker eingebunden ist
            # 
            # if data['accelerationTime']:
            #     movement.setAccelerationTime(data['accelerationTime'])
            # else:
            #     movement.setAccelerationTime(None)
            
            truck.save()
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

            # => sollte eingesetzt werden, sobald der Broker eingebunden ist
            # 
            # if data['accelerationTime']:
            #     movement.setAccelerationTime(data['accelerationTime'])
            # else:
            #     movement.setAccelerationTime(None)
            
            truck.save()
            success = True
        except:
            pass
        return JsonResponse({'success': success}, status=500)

    def emergencyBrake(self, request):
        success = False
        truck = TruckEntity.objects.get(pk=ID)
        try:
            data = JSONParser().parse(request)
            truck.acceleration = MIN_ACCELERATION
            truck.targetSpeed = MIN_SPEED

            # => sollte eingesetzt werden, sobald der Broker eingebunden ist
            # 
            # movement.setAccelerationTime(None)

            truck.save()
            success = True
        except:
            pass
        return JsonResponse({'success': success}, status=500)

    def poll(self, request):
        pass

    ####  ##### #   #     ##### ####  ##### #   #     ####  ##### #   # ##### #   # ##### #   #
    #   #   #   ##  #     #     #   # #     ##  #     #   # #   # #   # #     #   # #     ##  #
    ####    #   # # #     ##### ####  ##### # # #     ####  ##### #   # #     ##### ##### # # #
    #   #   #   #  ##     #     #   # #     #  ##     #   # #   # #   # #     #   # #     #  ##
    ####  ##### #   #     ##### ####  ##### #   #     #   # #   # ##### ##### #   # ##### #   #
