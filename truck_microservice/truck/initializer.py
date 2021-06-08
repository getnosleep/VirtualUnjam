from rest_framework import viewsets
from django.http import HttpResponse, JsonResponse
from .models import TruckEntity
from .serializer import Serializer
from .properties import ID

ERRMSG_UNINITIALIZED = 'Has the truck already been initialized?'

class Initializer(viewsets.ViewSet):
    def initialize(self, request):
        trucks = TruckEntity.objects.all()
        if trucks.exists():
            TruckEntity.objects.all().delete()
        
        truck = TruckEntity()
        
        # Hier sollten die requestparams noch eingelesen werden und in die jeweiligen Zellen geschrieben werden

        truck.save()

        try:
            serializer = Serializer(truck, many=False)
            truckJSON = serializer.data
            return JsonResponse(data=truckJSON, status=200)
        except:
            return HttpResponse('Oh shit, that\'s an awesome fail...', status=400)
    
    def truck(self, request):
        truck = TruckEntity.objects.get(pk=ID)
        if truck:
            serializer = Serializer(truck, many=False)
            truckJSON = serializer.data
            return JsonResponse(data=truckJSON, status=200)
        else:
            return HttpResponse(ERRMSG_UNINITIALIZED, status=404)
