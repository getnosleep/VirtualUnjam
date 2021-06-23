# library imports
from threading import Thread
from django.http import HttpResponse
from rest_framework import viewsets

# property imports
from .properties import ID

# persistence layer imports
from .models import TruckEntity

class Init(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        trucks = TruckEntity.objects.all()
        if trucks.exists():
            TruckEntity.objects.all().delete()
        truck = TruckEntity()
        truck.save()

def initialize():
    init = Init()
    init.start()

class Initializer(viewsets.ViewSet):
    def init(self, request):
        initialize()
        return HttpResponse(status=200)

