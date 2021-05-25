from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class SthThatBehavesLikeATruck(object):
    def __init__(self, address: str, truckId=None, convoyPosition=None, convoyLeaderId=None, speed=0.0, isBroken=False, isPolling=False, isDecelerating=False, isAccelerating=False):
        self.__address__ = address
        self.__truckId__ = self.__generateId__(address) if truckId == None else truckId
        self.__convoyLeaderId__ = convoyLeaderId
        self.__convoyPosition__ = convoyPosition
        self.__speed__ = speed
        self.__isBroken__ = isBroken
        self.__isPolling__ = isPolling
        ####  ##### #   #     ##### ####  ##### #   #     ####  ##### #   # ##### #   # ##### #   #
        #   #   #   ##  #     #     #   # #     ##  #     #   # #   # #   # #     #   # #     ##  #
 	    ####    #   # # #     ##### ####  ##### # # #     ####  ##### #   # #     ##### ##### # # #
  	    #   #   #   #  ##     #     #   # #     #  ##     #   # #   # #   # #     #   # #     #  ##
        ####  ##### #   #     ##### ####  ##### #   #     #   # #   # ##### ##### #   # ##### #   #
        self.__isDecelerating__ = isDecelerating
        self.__isAccelerating__ = isAccelerating

    def __generateId__(self, address):
        from time import time
        from hashlib import sha256

        hashstring = f'{address}truck{str(time())}'
        return sha256(hashstring.encode('utf-8')).hexdigest()
    
    def reInit(self):
        self.__convoyPosition__ = None
        self.__convoyLeaderId__ = None
        self.__speed__ = 0.0
        self.__isBroken__ = False
        self.__isPolling__ = False
        self.__isDecelerating__ = False
        self.__isAccelerating__ = False

    def getAddress(self): return self.__address__
    def getTruckId(self): return self.__truckId__

    def getConvoyPosition(self): return self.__convoyPosition__
    def setConvoyPosition(self, convoyPosition: int):
        self.__convoyPosition__ = convoyPosition
        pass

    def getConvoyLeaderId(self): return self.__convoyLeaderId__
    def setConvoyLeaderId(self, convoyLeaderId: str):
        self.__convoyLeaderId__ = convoyLeaderId
        pass

    def getSpeed(self): return self.__speed__
    def setSpeed(self, speed: float):
        self.__speed__ = speed
        pass

    def isBroken(self): return self.__isBroken__
    def toggleBroken(self):
        self.__isBroken__ = not self.__isBroken__
        pass

    def isPolling(self): return self.__isPolling__
    def togglePolling(self):
        self.__isPolling__ = not self.__isPolling__
        pass
    
    def isDecelerating(self): return self.__isDecelerating__
    def toggleDecelerating(self):
        self.__isDecelerating__ = not self.__isDecelerating__
        pass
    
    def isAccelerating(self): return self.__isAccelerating__
    def toggleAccelerating(self):
        self.__isAccelerating__ = not self.__isAccelerating__
        pass

    def setDependent(self, convoyLeaderId: str, convoyPosition: int):
        self.setConvoyLeaderId(convoyLeaderId=convoyLeaderId)
        self.setConvoyPosition(convoyPosition=convoyPosition)
        self.__isMember__ = True
        pass

    def setIndependent(self):
        self.__convoyLeaderId__ = None
        self.__convoyPosition__ = None
        self.__isMember__ = False
        pass

    def isMember(self): return self.__convoyPosition__ != None and self.__convoyLeaderId__ != None

    def isLeader(self): return self.__convoyLeaderId__ == self.__truckId__

Truck = SthThatBehavesLikeATruck("ABCDEFGHIJKLMNO - Fick die Henne, wie bekomme ich die Umgebungsvariablen hier raus? - QRSTUVWXYZ - OKAY HALT DEIN MAUL !!!")

class TruckEntity(models.Model):
    # Settings
    truckId = models.IntegerField(primary_key=True, validators=[MinValueValidator(1)])
    address = models.CharField(max_length=50)

    # Status
    targetDistance = models.PositiveIntegerField(default=20, validators=[MinValueValidator(1)])
    currentDistance = models.PositiveIntegerField(default=20, validators=[MinValueValidator(1)])
    targetSpeed = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(80.0)])
    currentSpeed = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(80.0)])
    broken = models.BooleanField(default=False)
    convoyLeader = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    convoyPosition = models.PositiveIntegerField(validators=[MinValueValidator(0)])

    # Current actions that shouldn't be persisted
    polling = models.BooleanField(default=False)
    accelerating = models.BooleanField(default=False)
    decelerating = models.BooleanField(default=False)

# import socket # Koennte die richtige Loesung sein...
