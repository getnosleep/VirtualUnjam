# library imports
from threading import Thread

# property imports
from ..properties import ID, MIN_ACCELERATION, MIN_SPEED

# persistence layer imports
from ..models import TruckEntity

# extern requests
from ..extern_api.trucks import convoyRequest

class Drive(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        if self.__selfCheck__():
            self.__closingCheck__()

    def __selfCheck__(self):
        truckOk = True
        truck = TruckEntity.objects.get(pk=ID)
        if truck.broken:
            truck.currentDistance = .0
            if truck.currentSpeed > 0:
                truck.acceleration = MIN_ACCELERATION
                truck.targetSpeed = MIN_SPEED
            truck.leadingTruckAddress = None
            truck.frontTruckAddress = None
            truck.backTruckAddress = None
            truck.position = None
            truck.polling = False
            truck.full_clean()
            truck.save()
            truckOk = False
        return truckOk

    def __closingCheck__(self):
        truck = TruckEntity.objects.get(pk=ID)
        frontTruckAddress = truck.frontTruckAddress
        
        pass

def startDrive():
    drive = Drive()
    drive.start()
