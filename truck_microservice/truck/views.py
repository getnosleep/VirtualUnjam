from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from .serializers import TruckSerializer
from .services import Service
from .drive import Drive
from .models import Truck

class TruckBehaviour(viewsets.ViewSet):
    def create(self, request):
        truck = request.truck
        try:
            serializer = TruckSerializer(data=truck)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(data=truck, status=status.HTTP_406_NOT_ACCEPTABLE)

    def alive(self, request, pk=None):
        result = True
        return Response(data=result, status=status.HTTP_200_OK)

    def accelerate(self, request, pk=None):
        truckId = request.truck_id
        speedOffset = request.speed_offset

        message = ''

        try:
            if Drive.changeSpeed(truckId=truckId, speed=speedOffset):
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response(status=status.HTTP_417_EXPECTATION_FAILED)

    def decelerate(self, request, pk=None):
        truckId = request.truck_id
        speedOffset = request.speed_offset

        message = ''

        try:
            if Drive.changeSpeed(truckId=truckId, speed=speedOffset):
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response(status=status.HTTP_417_EXPECTATION_FAILED)

    def stop(self, request, pk=None):
        truckId = request.truck_id

        message = ''

        try:
            #Service.stop(truckId=truckId)
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_412_PRECONDITION_FAILED)
        pass
    
    def joinConvoy(self, request, pk=None):
        truckId = request.truck_id
        convoyPosition = request.convoy_position

        message = ''

        try:
            Drive.changeConvoyPosition(truckId=truckId, newConvoyPosition=convoyPosition)
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def leaveConvoy(self, request, pk=None):
        pass

class TruckMonitoring(viewsets.ViewSet):
    def retrieve(self, request, pk=None): # monitoring interface - host:port/truck/<str:id>
        truckId = request.truck_id
        try:
            truck = Truck.objects.get(truckId=truckId)
            serializer = TruckSerializer(truck, many=False)
            if truck:
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #def speed_monitor ... etc -> because of CQRS
