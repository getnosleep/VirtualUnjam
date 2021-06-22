# Create your views here.
from .daemons.callbacks import Callbacks
import re

from rest_framework import viewsets, status
from django.http.response import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser

import concurrent.futures
import requests

# dirty imports
from .daemons.subscriber import subscription

def monitoring(addresses):
    def request(address):
        """@returns the status of the requested truck"""
        result = requests.get(address + 'api/monitor')
        return result.json()

    trucks = [] #jason list

    for address in addresses:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(request, address)
            trucks.append(future.result())

    return trucks

class Monitor(viewsets.ViewSet):

    requestlist = []
    addresses = set()

    def __addToAddresses__(self, address):
        #validirung mit pattern http://127.0.0.1:1031/
        address= "http://127.0.0.1:1031/"
        if (address[-1] == '/' and address[0:7] == "http://"):
            if (':' in address):
                ip = address[7:-1].split(":")
                if ([0 <= int(x) < 256 for x in
                     re.split('\.', re.match(r'^\d+\.\d+\.\d+\.\d+$', ip[0]).group(0))].count(True) == 4):
                    if(0 < int(ip[1]) < 65536):
                        pass #hier ist richtig ansosten nicht

        print(address)
        if address:
            self.addresses.add(address)
            return (True, 200)
        else: return (False, 400)

    def __deleteFromAddresses__(self, address):
        if address and address in self.addresses:
            self.addresses.remove(address)
            return (True, 200)
        else: return (False, 400)


    def activate(self, request):
        success = False
        status = 404
        try:
            data = JSONParser().parse(request)
            address = data['address']
            success, status = self.__addToAddresses__(address)
        except Exception as e:
            pass
        return HttpResponse(success, status=status)

    def deactivate(self, request):
        success = False
        status = 404
        try:
            data = JSONParser().parse(request)
            address = data['address']
            success, status = self.__deleteFromAddresses__(address)
        except Exception as e:
            pass
        return HttpResponse(success, status=status)



    def truckAdresses(self, request):
        try:
            data = {
                'data': list(self.addresses),
            }
            return JsonResponse(data, status=200)
        except Exception as e:
            pass
        return HttpResponse(status=400)


    '''
    def dataStacker(self, request):
        try:
            trucks = monitoring(self.addresses)
            data = {
                'data': trucks,
            }
            return JsonResponse(data, status=200)
        except Exception as e:
            return HttpResponse(e, status=500)
    '''

def dataStacker(self, request):
    try:
        data = {
            'data': Callbacks.truckDictionary
        }
        return JsonResponse(data, status=200)
    except Exception as e:
        return HttpResponse(e, status=500)