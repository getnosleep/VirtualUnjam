from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from .drive import Drive

class TruckBehaviour(viewsets.ViewSet):
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

"""
joinConvoy Methode
     anlegen und sobald der Truck einem Convoy joinen soll dementsprechend die Methode aufrufen und das Objekt hinsichtlich wder TruckID manipulieren

accelerate:
    setSpeed methode -> idempotent (ist validiert)
"""

