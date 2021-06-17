# library imports
from threading import Thread
from ..serializer import ConvoySerializer
from rest_framework.parsers import JSONParser
import time

# property imports
from ..properties import EMERGENCY_BRAKE, ID, MIN_ACCELERATION

# persistence layer imports
from ..models import TruckEntity

# extern requests
from ..extern_api.addresses import registered
from ..extern_api.trucks import convoyRequest

class Lifecycle(Thread):
    def __init__(self):
        Thread.__init__(self, daemon=True)

    def run(self):
        self.convoyUpdate()

    def convoyUpdate(self):
        truck = TruckEntity.objects.get(pk=ID)

        frontTruck = truck.frontTruckAddress
        backTruck = truck.backTruckAddress

        if frontTruck:
            truckInFront = self.__requestTruck__(frontTruck)
            if truckInFront:
                serialized = ConvoySerializer(data=truckInFront)
                if serialized.is_valid():
                    serialized.save()
            else:
                self.__frontTruckNotAccessible__()
        if backTruck:
            truckBehind = self.__requestTruck__(backTruck)
            if not truckBehind:
                self.__truckBehindNotAccessible__()

    def __requestTruck__(self, trucksAddress):
        try:
            otherTruck = convoyRequest(trucksAddress)
            if otherTruck.status_code == 200:
                truck = JSONParser().parse(otherTruck)
                if truck['position']:
                    return truck
        except:
            pass
        return False

    def __frontTruckNotAccessible__(self):
        truck = TruckEntity.objects.get(pk=ID)
        TruckEntity.objects.filter(address=truck.frontTruckAddress).delete()
        truck.frontTruckAddress = None
        truck.polling = True
        truck.save()

    def __truckBehindNotAccessible__(self):
        truck = TruckEntity.objects.get(pk=ID)
        truck.backTruckAddress = None
        truck.save()
