

from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from django.http.response import JsonResponse
from threading import Thread

class Monitorworker(Thread):
    def __init__(self):
        super().__init__()
        self.active = True

    def run(self):
        while self.active:
            pass

    def stop(self):
        self.active =False

    def reqTruck(selfs, adress):
        pass

class Monitor(viewsets.ViewSet):
    def test (self: viewsets.ViewSet, request: Request, pk=None) -> Response:
        try:
            if 1==1:
                data = {
                    'data': 100
                }
                return JsonResponse(data=data,status=200)
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def test2 (self: viewsets.ViewSet, request: Request, pk=None) -> Response:
        try:
            if 1==1:
                data = {
                    'data': 200
                }
                return JsonResponse(data=data,status=200)
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    def runtest (self: viewsets.ViewSet, request: Request, pk=None) -> Response:
        try:
            #os.system("manage.py runserver 127.0.0.1:8000")

            if 1==1:
                data = {
                    'data': 9000
                }
                return JsonResponse(data=data,status=200)
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def datastacker (self: viewsets.ViewSet, request: Request, pk=None) -> Response:
        try:
            #do somthing with data
            if 1==1:
                data = {
                    'data': 2000
                }
                return JsonResponse(data=data,status=200)
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)