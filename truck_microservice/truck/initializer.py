# library imports
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse, JsonResponse

# property imports
from .properties import ID

# persistence layer imports
from .models import TruckEntity
from .serializer import Serializer

class Initializer(viewsets.ViewSet):
    def init(self, request):
        trucks = TruckEntity.objects.all()
        if trucks.exists():
            TruckEntity.objects.all().delete()
        truck = TruckEntity()

        truck.save()
        serializer = Serializer(truck, many=False)
        truckJSON = serializer.data
        return JsonResponse(data=truckJSON, status=200)
    
    def truck(self, request):
        try:
            truck = TruckEntity.objects.all()#get(pk=ID)
            if truck:
                serializer = Serializer(truck, many=True)
                data = {
                    'trucks': serializer.data
                }
                return JsonResponse(data, status=200)
            else:
                return HttpResponse('Has the truck already been initialized?', status=404)
        except Exception as e:
            return HttpResponse('Erronimo => Maybe the Serializer', status=500)
