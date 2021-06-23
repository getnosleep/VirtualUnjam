# library imports
from threading import Thread
import time

# property imports
from ..properties import ID, ADDRESS_SELF

# persistence layer imports
from ..models import TruckEntity

# extern requests
from ..extern_api.addresses import overwriteRegistration, registered
from ..extern_api.trucks import bullyAcknowledgement, pollRequest, startBullying

def finishBullying(truckBehind, leader, oldPosition, newPosition):
    success = False

    # Inform the Convoy Microservice
    bullied = overwriteRegistration(oldPosition, newPosition)
    if bullied and bullied.status_code == 200:
        success = True
    
    # Inform the Truck behind
    if truckBehind:
        acknowledgement = bullyAcknowledgement(truckBehind, leader, newPosition)
        if not acknowledgement or not acknowledgement.status_code == 200:
            success = True
    
    return success

class BullyAlgorithm(Thread):
    def __init__(self):
        Thread.__init__(self, daemon=True)
        self.success = False
        self.failed = False
        self.tries = 0
    
    def run(self):
        while not self.failed and not self.success and self.tries < 3:
            self.__bully__()
            print('waiting')
            time.sleep(10)

    def __bully__(self):
        print('bully')
        registerRequest = registered()
        if registerRequest and registerRequest.status_code == 200:
            addresses = registerRequest.json()
            frontTruck = self.__findPosition__(addresses)
            if frontTruck == ADDRESS_SELF:
                print('imma leader now')
                self.__makeLeader__()
            else:
                print('imma follower')
                self.__actualizePosition__(frontTruck)
        else:
            self.tries += 1

    def __findPosition__(self, addresses: dict):
        """@returns the address of the truck in front and the position of own truck"""
        currentFrontTruck = ADDRESS_SELF
        position = 1
        
        # Iterate till you find own address
        for pos, address in addresses.items():
            if address == ADDRESS_SELF:
                return currentFrontTruck
            
            currentTruckRequest = pollRequest(address)
            # Increment / update for every responding truck
            if currentTruckRequest and currentTruckRequest.status_code == 200:
                currentTruck = currentTruckRequest.json()
                if currentTruck['position']:
                    currentFrontTruck = address
                    position += 1
        
        # In case of not reacting to own address
        self.failed = True
        return None

    def __makeLeader__(self):
        print('imma the new leader')
        """Sets leader attributes, gives acknowledgement to truck in back and overwrites the own convoy service position"""
        truck = TruckEntity.objects.get(pk=ID)

        # Caching the value for the overwrite
        oldPosition = truck.position
        truckBehind = truck.backTruckAddress

        # Close the bully chain
        success = finishBullying(truckBehind, ADDRESS_SELF, oldPosition, 1)
        print('success success success yaaaaaay')
        truck = TruckEntity.objects.get(pk=ID)
        truck.frontTruckAddress = None
        truck.position = 1
        truck.leadingTruckAddress = ADDRESS_SELF
        truck.save()

        if success:
            self.success = True
        else:
            self.tries += 1

    def __actualizePosition__(self, frontTruck):
        """Sets information of new truck in front and tells it to start polling"""
        truck = TruckEntity.objects.get(pk=ID)
        truck.frontTruckAddress = frontTruck
        truck.save()

        # Tell the truck in front to start bullying
        bullyChain = startBullying(frontTruck)
        if bullyChain and bullyChain.status_code == 200:
            self.success = True
        else:
            self.tries += 1
    
    def __deleteTruckBehind__(self):
        truck = TruckEntity.objects.get(pk=ID)
        truck.backTruckAddress = None
        truck.save()

def bully():
    bully = BullyAlgorithm()
    bully.start()
