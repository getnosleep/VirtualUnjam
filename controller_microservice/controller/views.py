# Create your views here.
import re

from rest_framework import viewsets
from django.http.response import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser

from zope.pagetemplate.pagetemplatefile import PageTemplateFile
from zope.pagetemplate.pagetemplate import PageTemplate
from django.template import Template, Context

# dirty imports
from .daemons.callbacks import Callbacks
from .daemons.subscriber import subscription

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
            <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Virtuel Unjam</title>
        <script src="doch.js"></script>
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

            </tbody>

        </table>
    <button onclick=sendit()>send JS </button>

    </body>
    </html>
            """

            t = Template(template)
            c = Context({"pos": 1,
                         "speed": 20,
                         "distance": 23462,
                         "pos1": 2,
                         "speed1": 22,
                         "distance1": 123262,
                         "pos2": 3,
                         "speed2": 502,
                         "distance2": 12123462,
                         })
            print(t.render(c))
            # pt = mypt()
            # pt.write(template)
            # pt=pt(truckdata=truckdata()).strip()
            # print(pt)
            # my_pt = PageTemplateFile("webPage.html")
            # my_pt = my_pt(truckdata=truckdata()).strip()
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





class truckdata(object):
    #todo hier alle truckdaten
    def listlen(self) :return [1,2]
    def getID(self) :return "2"
    def getSpeed(self) :
        for key, value in Callbacks.truckDictionary.items():
            pass

        return "80"
    def getDistance(self) :return "150374.0654204"


class mypt(PageTemplate):
    def pt_getContext(self, args=(), options={}, **kw):
       rval = PageTemplate.pt_getContext(self, args=args)
       options.update(rval)
       return options
