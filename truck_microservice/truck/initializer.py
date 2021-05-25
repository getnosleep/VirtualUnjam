from django.http.response import HttpResponse
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from .models import TruckEntity
from .serializer import TruckSerializer

TRUCK_ID = 0
ADDRESS = ''

class Initializer(viewsets.ViewSet):
    def initializeWithParams(self, request):
        """A function that wouldn\'t be necessary, if there were some hardware params to call.\nIn this case there is none, because these trucks aren\'t real\n(╯°□°)╯︵ ┻━┻"""
        try:
            data = JSONParser().parse(request)
            serializer = TruckSerializer(data=data)
            if serializer.is_valid():
                self.__flush__()
                serializer.save()
                TRUCK_ID = serializer.
        except:
            return HttpResponse(data='The given data isn\'t valide.', status=404)

    def initializeWithoutParams(self, request):
        try:
            trucks = TruckEntity.objects.all()
            if len(trucks) == 1:
                # Best Case: A database has already been initialized and we only need to fetch the data and register the truck
                pass
            elif len(trucks < 1):
                # Uninitialized Case: This will probably happen anyway, but to be functionally sure, we raise this
                raise Exception
            else:
                # Worst Case: The Database has a conflict and we need to flush it before we can recreate a truck and register it
                self.__flush__()
                raise Exception
        except:
            self.__setup__()
        finally:
            truckId, address = self.__register__()
            TRUCK_ID = truckId
            ADDRESS = address

    def __flush__(self):
        """Deletes all Database-Entries"""
        TruckEntity.objects.all().delete()
        pass

    def __setup__(self):
        """Creates a new Truck with standard settings"""
        data = {}
        serializer = TruckSerializer(data=data)
        if serializer.is_valid():
            self.__flush__()
            serializer.save()
            TRUCK_ID = serializer.

    def __register__(self):
        # register the truck on convoy
        pass

