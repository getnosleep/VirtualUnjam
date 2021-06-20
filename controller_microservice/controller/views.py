

# Create your views here.
from rest_framework import viewsets, status
from django.http.response import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
import concurrent.futures
import requests

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
        # todo validirung mit pattern
        if address:
            self.addresses.add(address)
            return (True, 200)
        else: return (False, 400)

    def __deleteFromAddresses__(self, address):
        # todo validirung ob da
        if address:
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



    def dataStacker(self, request):
        try:
            trucks = monitoring(self.addresses)
            data = {
                'data': trucks,
            }
            return JsonResponse(data, status=200)
        except Exception as e:
            return HttpResponse(e, status=500)