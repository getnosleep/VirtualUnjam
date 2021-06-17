# library imports
from .exceptions.invalid_input import AccelerationException
from django.core.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse

# property imports
from .properties import ID

# persistence layer imports
from .models import TruckEntity

# dirty imports
from .daemons.subscriber import subscription

# extern requests
from .extern_api.addresses import join, registered

# error messages
ERR_MSG_VALIDATION = 'Your input wasn\'t valid.'
ERR_MSG_ACCESSABILITY = 'Truck not accessible'
ERR_MSG_JOIN = 'Joining the convoy wasn\'t possible for unknown reason'
ERR_MSG_LEAVE = 'Leaving the convoy wasn\'t possible for unknown reason'

SUB = subscription

class Mutation(viewsets.ViewSet):
    def joinConvoy(self, request):
        try:
            status = join()
            return HttpResponse(status=status)
        except:
            return HttpResponse(ERR_MSG_JOIN, status=500)

    def leaveConvoy(self, request):
        try:
            truck = TruckEntity.objects.get(pk=ID)
            truck.position = None
            truck.leadingTruckAddress = None
            truck.frontTruckAddress = None
            truck.backTruckAddress = None
            truck.polling = False
            truck.closing = False

            # Maybe unwanted, but nice to see
            truck.targetSpeed = .0
            truck.acceleration = -1.0
            
            truck.full_clean()
            truck.save()
            return HttpResponse(status=200)
        except:
            return HttpResponse(ERR_MSG_LEAVE, status=500)

    def accelerate(self, request):
        success = False
        status = 500
        truck = TruckEntity.objects.get(pk=ID)
        if truck.leadingTruckAddress == truck.address or not truck.position:
            try:
                data = JSONParser().parse(request)
                
                acc = data['acceleration']
                vel = data['targetSpeed'] / 3.6

                if acc > .0 and vel > truck.currentSpeed or acc < .0 and vel < truck.currentSpeed:
                    truck.acceleration = acc
                    truck.targetSpeed = vel
                else:
                    raise AccelerationException()
                truck.full_clean()
                truck.save()
                success = True
                status = 200
            except ValidationError as e:
                return HttpResponse(ERR_MSG_VALIDATION, status=401)
            except AccelerationException as e:
                return HttpResponse(e.message, status=404)
        return JsonResponse({'success': success}, status=status)

    def poll(self, request):
        try:
            reg = registered()
            a = JSONParser().parse(reg)
            return HttpResponse(a, status=200)
        except Exception as e:
            return HttpResponse('unsuccessful', status=500)
