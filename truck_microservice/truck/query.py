from rest_framework import viewsets
from django.http import HttpResponse, JsonResponse

from .models import TruckEntity
from .serializer import TruckSerializer
from .exceptions.initialization import TruckNotInitializedException
from .properties import ID

ERRMSG_UNINITIALIZED = 'Has the truck already been initialized?'

class Query(viewsets.ViewSet):
    # def settings(self, request):
    #     print('za')
    #     try:
    #         truck = TruckEntity.objects.get(pk=ID)
    #         if truck.exists():
    #             data = {
    #                 'truckId': truck.truckId,
    #                 'address': truck.address,
    #             }
    #         return JsonResponse(data=data, status=200)
    #     except TruckNotInitializedException as e:
    #         return HttpResponse(e.message, status=204)
    #     except TruckEntity.DoesNotExist:
    #         return HttpResponse(ERRMSG_UNINITIALIZED, status=404)
    #     except:
    #         return HttpResponse('We are sorry, a problem has occured.', status=500)
    
    # def status(self, request):
    #     try:
    #         if ID > 0:
    #             truck = TruckEntity.objects.get(truckId = ID)
    #             data = {
    #                 'truckId': truck.truckId,
    #                 'targetDistance': truck.targetDistance,
    #                 'currentDistance': truck.currentDistance,
    #                 'targetSpeed': truck.targetSpeed,
    #                 'currentSpeed': truck.currentSpeed,
    #                 'broken': truck.broken,
    #                 'convoyLeader': truck.convoyLeader,
    #                 'convoyPosition': truck.convoyPosition,
    #             }
    #             return JsonResponse(data=data, status=200)
    #         else:
    #             raise TruckNotInitializedException
    #     except TruckNotInitializedException as e:
    #         return HttpResponse(e.message, status=204)
    #     except TruckEntity.DoesNotExist:
    #         return HttpResponse(ERRMSG_UNINITIALIZED, status=404)
    #     except:
    #         return HttpResponse('We are sorry, a problem has occured.', status=500)

    # def actions(self, request):
    #     try:
    #         if ID > 0:
    #             truck = TruckEntity.objects.get(truckId = ID)
    #             data = {
    #                 'polling': truck.polling,
    #                 'accelerating': truck.accelerating,
    #                 'decelerating': truck.decelerating,
    #             }
    #             return JsonResponse(data=data, status=200)
    #         else:
    #             raise TruckNotInitializedException
    #     except TruckNotInitializedException as e:
    #         return HttpResponse(e.message, status=204)
    #     except TruckEntity.DoesNotExist:
    #         return HttpResponse(ERRMSG_UNINITIALIZED, status=404)
    #     except:
    #         return HttpResponse('We are sorry, a problem has occured.', status=500)

    def truck(self, request):
        truck = TruckEntity.objects.get(pk=ID)
        if truck:
            serializer = TruckSerializer(truck, many=False)
            truckJSON = serializer.data
            return JsonResponse(data=truckJSON, status=200)
        else:
            return HttpResponse(ERRMSG_UNINITIALIZED, status=404)
