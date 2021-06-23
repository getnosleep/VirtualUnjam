# Create your views here.
import json
import re
import requests

from rest_framework import viewsets
from django.http.response import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser

from django.template import Template, Context

# dirty imports
from .daemons.callbacks import Callbacks
from .daemons.subscriber import subscription
from .properties import COUNT, INTERVAL, ID_BROKER, ADDRESS_BROKER, PORT_BROKER, USERNAME_BROKER, PASSWORD_BROKER, TOPIC_BROKER, TOPIC_TRUCKS, DURATION_BROKER, MAX_TIMEOUT, ADDRESS_HEARTBEAT 

class Mutation(viewsets.ViewSet):

    def jonConvoy(self, request):
        try:
            requestData = JSONParser().parse(request)
            truck = Callbacks.truckDictionary[requestData['id']]
            truckAddress = truck['address']
            headers = {'content-type': 'application/json'}
            val = requests.post('http://' + truckAddress + '/api/convoy', None, headers=headers, timeout=MAX_TIMEOUT)
            if val.status_code == 200:
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=400)
        except Exception as e:
            return HttpResponse(e.message, status=404)

    def leaveConvoy(self, request):
        try:
            requestData = JSONParser().parse(request)
            truck = Callbacks.truckDictionary[requestData['id']]
            truckAddress = truck['address']
            headers = {'content-type': 'application/json'}
            val = requests.delete('http://' + truckAddress + '/api/convoy', None, headers=headers, timeout=MAX_TIMEOUT)
            if val.status_code == 200:
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=400)
        except Exception as e:
            return HttpResponse(e.message, status=404)

    def repair(self, request):
        try:
            requestData = JSONParser().parse(request)
            truck = Callbacks.truckDictionary[requestData['id']]
            truckAddress = truck['address']
            headers = {'content-type': 'application/json'}
            val = requests.post('http://' + truckAddress + '/api/intact', None, headers=headers, timeout=MAX_TIMEOUT)
            if val.status_code == 200:
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=400)
        except Exception as e:
            return HttpResponse(e.message, status=404)

    def destroy(self, request):
        try:
            requestData = JSONParser().parse(request)
            truck = Callbacks.truckDictionary[requestData['id']]
            truckAddress = truck['address']
            headers = {'content-type': 'application/json'}
            val = requests.delete('http://' + truckAddress + '/api/intact', None, headers=headers, timeout=MAX_TIMEOUT)
            if val.status_code == 200:
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=400)
        except Exception as e:
            return HttpResponse(e.message, status=404)

    def accelerate(self, request):
        try:
            requestData = JSONParser().parse(request)
            truck = Callbacks.truckDictionary[requestData['id']]
            truckAddress = truck['address']
            headers = {'content-type': 'application/json'}
            data = {
                'targetSpeed': requestData['targetSpeed'],
                'acceleration': requestData['acceleration']
            }
            val = requests.post('http://' + truckAddress + '/api/accelerate', data=json.dumps(data), headers=headers, timeout=MAX_TIMEOUT)
            if val.status_code == 200:
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=400)
        except Exception as e:
            return HttpResponse(e.message, status=404)

    def inject(self, request):
        try:
            headers = {'content-type': 'application/json'}
            data = {
                "interval": INTERVAL,
                "count": COUNT,
                "broker_address": ADDRESS_BROKER,
                "broker_port": PORT_BROKER,
                "broker_username": USERNAME_BROKER,
                "broker_password": PASSWORD_BROKER,
                "broker_channel": TOPIC_TRUCKS
            }
            val = requests.post('http://' + ADDRESS_HEARTBEAT + '/heartbeat/needle', data=json.dumps(data), headers=headers, timeout=MAX_TIMEOUT)
            if val.status_code == 200:
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=400)
        except Exception as e:
            return HttpResponse(e.message, status=404)

    def flatline(self, request):
        try:
            headers = {'content-type': 'application/json'}
            val = requests.delete('http://' + ADDRESS_HEARTBEAT + '/heartbeat/needle', None, headers=headers, timeout=MAX_TIMEOUT)
            if val.status_code == 200:
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=400)
        except Exception as e:
            return HttpResponse(e.message, status=404)
class Monitor(viewsets.ViewSet):

    requestlist = []
    addresses = set()

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
                <th>position</th>
                <th>id </th>
                <th>length</th>
                <th>broken</th>
                <th>polling</th>
                <th>closing</th>
                <th>accelerating</th>
                <th>decelerating</th>
                <th>currentSpeed</th>
                <th>currentDistance</th>
                <th>currentRouteSection</th>
                <th>targetRouteSection</th> 	 	
            </tr>
            </thead>

            <tbody>
                <tr>
                {% for value in da.values %}
                <td>
                    {% for k, v in value.items %}
                        {{ v }}
                        <td>
                    {% endfor %} 
                </tr>
                {% endfor %}

            </tbody>

        </table>
    <button onclick=sendit()>send JS </button>
    <button onclick=accelerate()>accelerate</button>
    <input type="text" name="accelerateFeld" id="accelerate_Feld" onclick="this.value=' '" value="truckID">
    <button onclick=decelerate()>decelerate</button>
    <button onclick=destroy()>destroy</button>
    <button onclick=repair()>repair</button>
    <button onclick=joinConvoy()>joinConvoy</button>
    <button onclick=leaveConvoy()>leaveConvoy</button>
    


    </body>
    </html>
            """
            truck1=[]
            for value in Callbacks.truckDictionary.values():
                print(value)
                truck1.append(value['id'])
                truck1.append(value['position'])
                truck1.append(value['currentSpeed']*3.6)
                truck1.append(value['currentRouteSection'])
                print(value['position'])

            t = Template(template)
            #c = Context({"id": truck1[0],
            #             "pos": truck1[1],
            #             "speed": truck1[2],
            #             "distance": truck1[3],
            #             "pos1": 2,
            #             "speed1": 22,
            #             "distance1": 123262,
            #             "pos2": 3,
            #             "speed2": 502,
            #             "distance2": 12123462,
            #             })
            c = Context({"da": Callbacks.truckDictionary
                         })
            #print(t.render(c))
            return HttpResponse(t.render(c), status=200)
