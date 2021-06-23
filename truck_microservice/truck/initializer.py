# library imports
from rest_framework import viewsets
from django.http import HttpResponse

# property imports
from .properties import ID

# persistence layer imports
from .models import TruckEntity

class Initializer(viewsets.ViewSet):
    def init(self, request):
        try:
            trucks = TruckEntity.objects.all()
            if trucks.exists():
                TruckEntity.objects.all().delete()
            truck = TruckEntity()
            truck.save()
            return HttpResponse(status=200)
        except Exception as e:
            print(e)
            HttpResponse(status=400)
