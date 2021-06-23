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

        leader = not truck.frontTruckAddress and truck.address == truck.leadingTruckAddress
        lonely = not (truck.frontTruckAddress or truck.backTruckAddress)

        if lonely:
            pass
        elif leader:
            self.__accessTruckBehind__(backTruck)
        else:
            if backTruck:
                self.__accessTruckBehind__(backTruck)
            if frontTruck:
                self.__accessTruckInFront__(frontTruck)

    def __accessTruckBehind__(self, backTruck):
        truckBehind = convoyRequest(backTruck)
        if truckBehind and truckBehind.status_code == 200:
            if self.__truckBehindAlignment__(truckBehind.json()):
                return True
        truck = TruckEntity.objects.get(pk=ID)
        truck.backTruckAddress = None
        truck.save()
        return False
    
    def __truckBehindAlignment__(self, truckBehind):
        truck = TruckEntity.objects.get(pk=ID)
        if truckBehind['position']:
            return True
        return False

    def __accessTruckInFront__(self, frontTruck):
        truckInFront = convoyRequest(frontTruck)
        if truckInFront and truckInFront.status_code == 200:
            if self.__truckInFrontAlignment__(truckInFront.json()):
                return True
        
        truck = TruckEntity.objects.get(pk=ID)
        truck.frontTruckAddress = None
        if not truck.polling:
            truck.polling = True
            bully()
        truck.save()
        return False

    def __truckInFrontAlignment__(self, truckInFront):
        truck = TruckEntity.objects.get(pk=ID)
        return truck.polling or truckInFront['polling'] or truckInFront['position'] and truckInFront['position'] < truck.position and truckInFront['leadingTruckAddress'] == truck.leadingTruckAddress

def startLifecycle():
    lifecycle = Lifecycle()
    lifecycle.start()
