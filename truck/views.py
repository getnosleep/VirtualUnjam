from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from .serializers import TruckSerializer
from .services import service
from .models import Truck

# Trucks view set class.
class TruckBehaviour(viewsets.ViewSet):
    def alive(self, request, pk=None):
        result = True
        return Response(data=result, status=status.HTTP_200_OK)

    def accelerate(self, request, pk=None):
        truckId = request.truck_id
        speedOffset = request.speed_offset

        message = ''

        try:
            if service.changeSpeed(truckId=truckId, speedOffset=speedOffset):
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
            if service.changeSpeed(truckId=truckId, speedOffset=speedOffset):
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response(status=status.HTTP_417_EXPECTATION_FAILED)

    def stop(self, request, pk=None):
        truckId = request.truck_id

        message = ''

        try:
            #service.stop(truckId=truckId)
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_412_PRECONDITION_FAILED)
        pass
    
    def joinConvoy(self, request, pk=None):
        truckId = request.truck_id
        convoyPosition = request.convoy_position

        message = ''

        try:
            service.changeConvoyPosition(truckId=truckId, newConvoyPosition=convoyPosition)
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def leaveConvoy(self, request, pk=None):
        pass

class TruckMonitoring(viewsets.ViewSet):
    def retrieve(self, request, pk=None): # monitoring interface - host:port/truck/<str:id>
        truckId = request.truck_id
        truck = Truck.objects.get(truckId=truckId)
        serializer = TruckSerializer(truck, many=False)
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
