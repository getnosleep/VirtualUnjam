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

                speedSelf = truck.currentSpeed
                sectionSelf = truck.currentRouteSection
                distanceSelf = truck.distance

                destroy = False
                close = False
                t = 3 * DURATION_BROKER

                if sectionFrontTruck > sectionSelf:
                    # Best case -> correct ordering
                    currentDistance = sectionFrontTruck - lengthFrontTruck - sectionSelf
                    if currentDistance < distanceSelf and currentDistance > .0:
                        close = False
                    elif currentDistance > distanceSelf + (speedSelf - speedFrontTruck) * t:
                        close = True
                    elif currentDistance <= .0:
                        destroy = True
                elif sectionFrontTruck < sectionSelf:
                    # Worst case -> wrong ordering
                    self.__leave__()
                    return False
                else:
                    currentDistance = 0
                    if speedSelf * 3.6 > 10 or speedFrontTruck * 3.6 > 10:
                        destroy = True
                    close = False
                
                if destroy:
                    truck = TruckEntity.objects.get(pk=ID)
                    truck.broken = True
                    truck.full_clean()
                    truck.save()
                    crashTruck(frontTruckAddress)
                    return False
                elif close:
                    targetSpeed = targetSpeedFrontTruck + 5
                    if targetSpeed > MAX_SPEED:
                        targetSpeed = MAX_SPEED
                    acceleration = accelerationFrontTruck + 0.5
                    if acceleration > MAX_ACCELERATION:
                        acceleration = MAX_ACCELERATION
                    truck = TruckEntity.objects.get(pk=ID)
                    truck.targetSpeed = targetSpeed
                    truck.acceleration = acceleration
                    truck.full_clean()
                    truck.save()
                    return True
                else:
                    truck = TruckEntity.objects.get(pk=ID)
                    # truck.currentSpeed = speedFrontTruck
                    truck.acceleration = accelerationFrontTruck
                    truck.targetSpeed = targetSpeedFrontTruck
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
