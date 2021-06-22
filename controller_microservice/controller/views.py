# Create your views here.
import re
import requests

from rest_framework import viewsets
from django.http.response import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser

from django.template import Template, Context

# dirty imports
from .daemons.callbacks import Callbacks
from .daemons.subscriber import subscription
from .properties import MAX_TIMEOUT

class Mutation(viewsets.ViewSet):

    def jonConvoy(self, request):
        try:
            requestData = JSONParser().parse(request)
            headers = {'content-type': 'application/json'}
            val = requests.post('http://' + requestData.truckAddress + '/truck/convoy', None, headers=headers, timeout=MAX_TIMEOUT)
            if val.status_code == 200:
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=400)
        except Exception as e:
            return HttpResponse(e.message, status=404)

    def leaveConvoy(self, request):
        try:
            requestData = JSONParser().parse(request)
            headers = {'content-type': 'application/json'}
            val = requests.delete('http://' + requestData.truckAddress + '/truck/convoy', None, headers=headers, timeout=MAX_TIMEOUT)
            if val.status_code == 200:
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=400)
        except Exception as e:
            return HttpResponse(e.message, status=404)

    def repair(self, request):
        try:
            requestData = JSONParser().parse(request)
            headers = {'content-type': 'application/json'}
            val = requests.post('http://' + requestData.truckAddress + '/truck/intact', None, headers=headers, timeout=MAX_TIMEOUT)
            if val.status_code == 200:
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=400)
        except Exception as e:
            return HttpResponse(e.message, status=404)

    def destroy(self, request):
        try:
            requestData = JSONParser().parse(request)
            headers = {'content-type': 'application/json'}
            val = requests.delete('http://' + requestData.truckAddress + '/truck/intact', None, headers=headers, timeout=MAX_TIMEOUT)
            if val.status_code == 200:
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=400)
        except Exception as e:
            return HttpResponse(e.message, status=404)

    def accelerate(self, request):
        try:
            requestData = JSONParser().parse(request)
            headers = {'content-type': 'application/json'}
            val = requests.delete('http://' + requestData.truckAddress + '/truck/accelerate', None, headers=headers, timeout=MAX_TIMEOUT)
            if val.status_code == 200:
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=400)
        except Exception as e:
            return HttpResponse(e.message, status=404)

class Monitor(viewsets.ViewSet):

    requestlist = []
    addresses = set()

    def __addToAddresses__(self, address):
        #validirung http://127.0.0.1:1031/
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

    def web(self, request):
            template = """
            {% load static %}
            <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Virtuel Unjam</title>
        <script src="{% static 'doch.js' %}"></script>
    <style>
      table, th {
       border: 3px solid black;
       height: 40px;
       }
    </style>

    </head>
    <body>
    <header>
        <p text="Virtuel Unjam"/>
    </header>
    <table style="width:80% ">
            <thead>
            <tr>
                <th>truckpos</th>
                <th>speed</th>
                <th>distance</th>
            </tr>
            </thead>

            <tbody>
            <tr>
                <td >{{pos}}</td>
                <td >{{speed}}</td>
                <td >{{distance}}</td>
            </tr>
            <tr>
                <td >{{pos1}}</td>
                <td >{{speed1}}</td>
                <td >{{distance1}}</td>
            </tr>
            <tr>
                <td >{{pos2}}</td>
                <td >{{speed2}}</td>
                <td >{{distance2}}</td>
            </tr>
            <tr>
                <td >{{pos3}}</td>
                <td >{{speed3}}</td>
                <td >{{distance3}}</td>
            </tr>
            <tr>
                <td >{{pos4}}</td>
                <td >{{speed4}}</td>
                <td >{{distance4}}</td>
            </tr>

            </tbody>

        </table>
    <button onclick=sendit()>send JS </button>

    </body>
    </html>
            """
            truck1=[]
            for value in Callbacks.truckDictionary.values():
                print(value)
                truck1.append(value['position'])
                truck1.append(value['currentSpeed'])
                truck1.append(value['currentRouteSection'])
                print(value['position'])

            t = Template(template)
            c = Context({"pos": truck1[0],
                         "speed": truck1[1]*3.6,
                         "distance": truck1[2],
                         "pos1": 2,
                         "speed1": 22,
                         "distance1": 123262,
                         "pos2": 3,
                         "speed2": 502,
                         "distance2": 12123462,
                         })
            #print(t.render(c))
            return HttpResponse(t.render(c), status=200)


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



