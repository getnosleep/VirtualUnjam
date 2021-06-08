# library imports
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse

# property imports
from .properties import ID, ADDRESS, LENGTH

# persistence layer imports
from .models import TruckEntity
from .serializer import Serializer

# error messages
ERR_MSG_PARSER = 'Parsing the JSON-Body wasn\'t successful.'
ERR_MSG_INITIALIZATION = 'Has the truck already been initialized?'

class Initializer(viewsets.ViewSet):
    def recommendedInit(self, request):
        trucks = TruckEntity.objects.all()
        if trucks.exists():
            TruckEntity.objects.all().delete()
        truck = TruckEntity()
        truck.save()
        serializer = Serializer(truck, many=False)
        truckJSON = serializer.data
        return JsonResponse(data=truckJSON, status=200)

    def specificInit(self, request):
        trucks = TruckEntity.objects.all()
        if trucks.exists():
            TruckEntity.objects.all().delete()
        try:
            data = JSONParser.parse(request)

            truck = TruckEntity()
            truck.id = ID
            truck.address = ADDRESS
            truck.length = LENGTH

            """
            'currentRouteSection',
            'currentSpeed',
            'currentAcceleration',
            'targetRouteSection',
            'targetSpeed',


            watch the comment below... The order, is necessary... watch the serializer -> .serializer.Serializer to understand
            """

            truck.polling = False
            truck.broken = False

            """
            'convoyLeader',
            'convoyPosition',


            make it like:

            if data.convoyLeader:
                truck.convoyLeader = data.convoyLeader

            if convoyPosition:
                ...

            but don't be upset if my synthax was wrong...
            """

            truck.save()
            serializer = Serializer(truck, many=False)
            truckJSON = serializer.data
            return JsonResponse(data=truckJSON, status=200)
        except:
            HttpResponse(ERR_MSG_PARSER, status=404)
    
    def truck(self, request):
        truck = TruckEntity.objects.get(pk=ID)
        if truck:
            serializer = Serializer(truck, many=False)
            truckJSON = serializer.data
            return JsonResponse(data=truckJSON, status=200)
        else:
            return HttpResponse(ERR_MSG_INITIALIZATION, status=404)
