# library imports
from threading import Thread

# property imports
from ..properties import ID

# functional imports
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
                self.__accessTruckInFront__(frontTruck)

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
        truck.frontTruckAddress = None
        if not truck.polling:
            truck.polling = True
            bully()
        truck.save()
        return False

    def __truckAlignment__(self, truckInFront):
        # TODO hier muss der Movement-Abgleich hin
        truck = TruckEntity.objects.get(pk=ID)
        if truck.polling or truckInFront['polling'] or truckInFront['position'] and truckInFront['position']+1 == truck.position and truckInFront['leadingTruckAddress'] == truck.leadingTruckAddress:
            return True
        else:
            return False

def alive():
    lifecycle = Lifecycle()
    lifecycle.start()
