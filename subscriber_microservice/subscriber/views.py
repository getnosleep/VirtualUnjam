# Create your views here.
"""[Docstring] Holds microservice's views."""
from .exceptions import SubscriberConnectionException, SubscribeException
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
    
    def initializeSubscription(self: viewsets.ViewSet, request: Request, pk=None) -> Response:
        """[Docstring] Declares functions, starting the subscription."""
        try:
            data = JSONParser().parse(request)
            if len(data) != 5 or not 'broker_address' in data or not 'broker_port' in data or not 'broker_username' in data or not 'broker_password' in data or not 'broker_channel' in data:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
            brokerAddress = data['broker_address']
            brokerPort = data['broker_port']
            brokerUsername = data['broker_username']
            brokerPassword = data['broker_password']
            brokerChannel = data['broker_channel']
            if Service.subscribe(brokerAddress=brokerAddress, brokerPort=brokerPort, brokerUsername=brokerUsername, brokerPassword=brokerPassword, brokerChannel=brokerChannel):
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response(status=status.HTTP_417_EXPECTATION_FAILED)

    def stopSubscription(self: viewsets.ViewSet, request: Request, pk=None) -> Response:
        """[Docstring] Declares functions, stopping the heartbeats."""
        try:
            if Service.unsubscribe():
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
