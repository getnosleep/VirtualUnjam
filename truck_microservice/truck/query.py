from rest_framework import viewsets
from django.http import HttpResponse, JsonResponse

from .models import TruckEntity
from .serializer import TruckSerializer
from .exceptions.initialization import TruckNotInitializedException
from .initializer import TRUCK_ID

ERR = 0
ERRMSG_UNINITIALIZED = 'Please wait a few seconds until the initializer initialized this truck.'
ERRMSG_USELESS = 'Please kill me !!!'

class Query(viewsets.ViewSet):
    def settings(self, request):
        try:
            if TRUCK_ID > 0:
                truck = TruckEntity.objects.get(truckId = TRUCK_ID)
                data = {
                    'truckId': truck.truckId,
                    'address': truck.address,
                }
                return JsonResponse(data=data, status=200)
            else:
                raise TruckNotInitializedException
        except TruckNotInitializedException as e:
            return HttpResponse(e.message, status=204)
        except TruckEntity.DoesNotExist:
            if ERR > 3:
                return HttpResponse(ERRMSG_USELESS, status=404)
            ERR += 1
            return HttpResponse(ERRMSG_UNINITIALIZED, status=404)
        except:
            return HttpResponse('We are sorry, a problem has occured.', status=500)
    
    def status(self, request):
        try:
            if TRUCK_ID > 0:
                truck = TruckEntity.objects.get(truckId = TRUCK_ID)
                data = {
                    'truckId': truck.truckId,
                    'targetDistance': truck.targetDistance,
                    'currentDistance': truck.currentDistance,
                    'targetSpeed': truck.targetSpeed,
                    'currentSpeed': truck.currentSpeed,
                    'broken': truck.broken,
                    'convoyLeader': truck.convoyLeader,
                    'convoyPosition': truck.convoyPosition,
                }
                return JsonResponse(data=data, status=200)
            else:
                raise TruckNotInitializedException
        except TruckNotInitializedException as e:
            return HttpResponse(e.message, status=204)
        except TruckEntity.DoesNotExist:
            if ERR > 3:
                return HttpResponse(ERRMSG_USELESS, status=404)
            ERR += 1
            return HttpResponse(ERRMSG_UNINITIALIZED, status=404)
        except:
            return HttpResponse('We are sorry, a problem has occured.', status=500)

    def actions(self, request):
        try:
            if TRUCK_ID > 0:
                truck = TruckEntity.objects.get(truckId = TRUCK_ID)
                data = {
                    'polling': truck.polling,
                    'accelerating': truck.accelerating,
                    'decelerating': truck.decelerating,
                }
                return JsonResponse(data=data, status=200)
            else:
                raise TruckNotInitializedException
        except TruckNotInitializedException as e:
            return HttpResponse(e.message, status=204)
        except TruckEntity.DoesNotExist:
            if ERR > 3:
                return HttpResponse(ERRMSG_USELESS, status=404)
            ERR += 1
            return HttpResponse(ERRMSG_UNINITIALIZED, status=404)
        except:
            return HttpResponse('We are sorry, a problem has occured.', status=500)

    def truck(self, request):
        try:
            if TRUCK_ID > 0:
                truck = TruckEntity.objects.get(truckId = TRUCK_ID)
                serializedTruck = TruckSerializer(truck, many=False)
                return JsonResponse(data=serializedTruck.data, status=200)
            else:
                raise TruckNotInitializedException
        except TruckNotInitializedException as e:
            return HttpResponse(e.message, status=204)
        except TruckEntity.DoesNotExist:
            if ERR > 3:
                return HttpResponse(ERRMSG_USELESS, status=404)
            ERR += 1
            return HttpResponse(ERRMSG_UNINITIALIZED, status=404)
        except:
            return HttpResponse('We are sorry, a problem has occured.', status=500)
