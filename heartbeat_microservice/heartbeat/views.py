"""[Docstring] Holds microservice's views."""
from .exceptions import HeartbeatConnectionException, HeartbeatPublishException
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from .service import Service

from paho.mqtt.client import Client, MQTT_ERR_NO_CONN, MQTTv311
from django.shortcuts import render
from django.urls import path
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.request import Request

# Create your views here.
class Initializer(viewsets.ViewSet):
    """[Docstring] Declares view, handling respective api calls."""
    
    def initializeHeartbeats(self: viewsets.ViewSet, request: Request, pk=None):
        """[Docstring] Declares functions, stimulating heartbeats."""
        data = JSONParser().parse(request)
        if not data:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        interval = data['interval']
        count = data['count']
        brokerAddress = data['broker_address']
        brokerPort = data['broker_port']
        brokerUsername = data['broker_username']
        brokerPassword = data['broker_password']
        brokerChannel = data['broker_channel']
        try:
            if Service.initiateHeartbeat(interval=interval, count=count, brokerAddress=brokerAddress, brokerPort=brokerPort, brokerUsername=brokerUsername, brokerPassword=brokerPassword, brokerChannel=brokerChannel):
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        except HeartbeatConnectionException:
            return Response(status=status.HTTP_502_BAD_GATEWAY)
        except HeartbeatPublishException:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except:
            return Response(status=status.HTTP_417_EXPECTATION_FAILED)

    def stopHeartbeats(self: viewsets.ViewSet, request: Request, pk=None):
        """[Docstring] Declares functions, stopping the heartbeats."""
        try:
            if Service.stopHeartbeat():
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        except HeartbeatConnectionException:
            return Response(status=status.HTTP_502_BAD_GATEWAY)
        except HeartbeatPublishException:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except:
            return Response(status=status.HTTP_417_EXPECTATION_FAILED)

class Monitor(viewsets.ViewSet):
    """[Docstring] Declares view, handling respective api calls."""

    def monitorHeartbeats(self: viewsets.ViewSet, request: Request, pk=None):
        """[Docstring] Declares functions, publishing the heartbeat."""
        try:
            heartbeats: int = Service.monitorHeartBeat()
            if heartbeats:
                data = {
                    'heartbeats': heartbeats
                }
                return JsonResponse(data=data, status=200)
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

class HeartbeatBehaviour(viewsets.ViewSet):
    """[Docstring] Declares view, handling respective api calls."""

    def stopHeartbeat(self: viewsets.ViewSet, request: Request, pk=None):
        """[Docstring] Declares functions, publishing the heartbeat."""
        try:
            if Service.stopHeartbeat():
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response(status=status.HTTP_417_EXPECTATION_FAILED)
