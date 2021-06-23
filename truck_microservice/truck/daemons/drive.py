# library imports
from threading import Thread

# property imports
from ..properties import ID, MAX_ACCELERATION, MAX_SPEED, MIN_ACCELERATION, MIN_SPEED, DURATION_BROKER

# persistence layer imports
from ..models import TruckEntity

# extern requests
from ..extern_api.trucks import convoyRequest, crashTruck

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
        if frontTruckAddress:
            frontTruckRequest = convoyRequest(frontTruckAddress)
            if frontTruckRequest and frontTruckRequest.status_code == 200:
                frontTruck = frontTruckRequest.json()
                
                speedFrontTruck = frontTruck['currentSpeed']
                lengthFrontTruck = frontTruck['length']
                sectionFrontTruck = frontTruck['currentRouteSection']
                accelerationFrontTruck = frontTruck['acceleration']
                targetSpeedFrontTruck = frontTruck['targetSpeed']
                                
                truck = TruckEntity.objects.get(pk=ID)

                sectionSelf = truck.currentRouteSection
                distanceSelf = truck.distance

                if sectionFrontTruck <= distanceSelf + lengthFrontTruck:
                    return False
                elif sectionFrontTruck >= sectionSelf:
                    # Best case -> correct ordering
                    currentSection = sectionFrontTruck - distanceSelf - lengthFrontTruck
                    distance = distanceSelf + lengthFrontTruck
                elif sectionFrontTruck < sectionSelf:
                    # Worst case -> wrong ordering
                    self.__leave__()
                    return False
                
                truck = TruckEntity.objects.get(pk=ID)
                truck.currentSpeed = speedFrontTruck
                truck.acceleration = accelerationFrontTruck
                truck.targetSpeed = targetSpeedFrontTruck
                truck.currentRouteSection = currentSection
                truck.currentDistance = distance
                truck.full_clean()
                truck.save()
                return True
        return False

    def __leave__(self):
        truck = TruckEntity.objects.get(pk=ID)
        truck.currentDistance = .0
        truck.leadingTruckAddress = None
        truck.frontTruckAddress = None
        truck.backTruckAddress = None
        truck.position = None
        truck.polling = False
        truck.full_clean()
        truck.save()
    
def startDrive():
    drive = Drive()
    drive.start()
