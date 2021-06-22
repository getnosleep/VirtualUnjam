# library imports
from threading import Thread

# property imports
from ..properties import ID

# functional imports
from ..serializer import ConvoySerializer
from .bully import bully

# persistence layer imports
from ..models import TruckEntity

# extern requests
from ..extern_api.trucks import convoyRequest

class Lifecycle(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        self.__convoyUpdate__()

    def __convoyUpdate__(self):
        truck = TruckEntity.objects.get(pk=ID)

        frontTruck = truck.frontTruckAddress
        backTruck = truck.backTruckAddress

        leader = not frontTruck and backTruck
        lonely = not (frontTruck or backTruck)

        if lonely:
            pass
        elif leader:
            self.__accessTruckBehind__(backTruck)
        else:
            # TODO ggf. parallelisieren
            if backTruck:
                self.__accessTruckBehind__(backTruck)
            if frontTruck:
                accessible = self.__accessTruckInFront__(frontTruck)
                if not accessible:
                    bully()

    def __accessTruckBehind__(self, backTruck):
        truckBehind = convoyRequest(backTruck)
        if not truckBehind or not truckBehind.status_code == 200:
            truck = TruckEntity.objects.get(pk=ID)
            truck.backTruckAddress = None
            truck.save()

    def __accessTruckInFront__(self, frontTruck):
        truckInFront = convoyRequest(frontTruck)
        if truckInFront and truckInFront.status_code == 200:
            if self.__truckAlignment__(truckInFront.json()):
                return True
        truck = TruckEntity.objects.get(pk=ID)
        TruckEntity.objects.filter(address=truck.frontTruckAddress).delete()
        truck.frontTruckAddress = None
        truck.polling = True
        truck.save()
        return False

    def __truckAlignment__(self, truck):
        # TODO hier muss der Movement-Abgleich hin
        return False

def alive():
    lifecycle = Lifecycle()
    lifecycle.start()
