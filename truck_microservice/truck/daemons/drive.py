# library imports
from threading import Thread

# property imports
from ..properties import ID

# persistence layer imports
from ..models import TruckEntity

# extern requests
from ..extern_api.trucks import convoyRequest

class Drive(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        self.__convoyUpdate__()

    def __convoyUpdate__(self):
        truck = TruckEntity.objects.get(pk=ID)
        return self.__speedCheckTruckInFront__(truck.frontTruckAddress)

    def __speedCheckTruckInFront__(self, frontTruck):
        if frontTruck:
            truckInFront = convoyRequest(frontTruck)
            if truckInFront and truckInFront.status_code == 200:
                return True
        return False

def startDrive():
    drive = Drive()
    drive.start()
