"""[Docstring] Holds microservice's views."""
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from .service import Service

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.request import Request

class Initializer(viewsets.ViewSet):
    """[Docstring] Declares view, handling respective api calls."""
    def initializeHeartbeats(self: viewsets.ViewSet, request: Request, pk=None) -> Response:
        """[Docstring] Declares functions, stimulating heartbeats."""
        try:
            data = JSONParser().parse(request)
            if len(data) != 7 or not 'interval' in data or not 'count' in data or not 'broker_address' in data or not 'broker_port' in data or not 'broker_username' in data or not 'broker_password' in data or not 'broker_channel' in data or data['count'] < 0:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
            interval = data['interval']
            count = data['count']
            brokerAddress = data['broker_address']
            brokerPort = data['broker_port']
            brokerUsername = data['broker_username']
            brokerPassword = data['broker_password']
            brokerChannel = data['broker_channel']
            if Service.initiateHeartbeat(interval=interval, count=count, brokerAddress=brokerAddress, brokerPort=brokerPort, brokerUsername=brokerUsername, brokerPassword=brokerPassword, brokerChannel=brokerChannel):
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response(status=status.HTTP_417_EXPECTATION_FAILED)

    def stopHeartbeats(self: viewsets.ViewSet, request: Request, pk=None) -> Response:
        """[Docstring] Declares functions, stopping the heartbeats."""
        try:
            if Service.stopHeartbeat():
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response(status=status.HTTP_417_EXPECTATION_FAILED)

class Monitor(viewsets.ViewSet):
    """[Docstring] Declares view, handling respective api calls."""
    def monitorHeartbeats(self: viewsets.ViewSet, request: Request, pk=None) -> Response:
        """[Docstring] Declares functions, monitoring the heartbeat."""
        try:
            heartbeats: int = Service.monitorHeartbeat()
            if heartbeats:
                data = {
                    'heartbeats': heartbeats
                }
                return JsonResponse(data=data, status=200)
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
