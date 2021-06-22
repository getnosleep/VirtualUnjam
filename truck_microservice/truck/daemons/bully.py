# library imports
from threading import Thread

# property imports
from ..properties import ID, ADDRESS_SELF

# persistence layer imports
from ..models import TruckEntity

# extern requests
from ..extern_api.addresses import overwriteRegistration, registered
from ..extern_api.trucks import bullyAcknowledgement, pollRequest, startBullying

def sort(dictionary: dict):
    return {key: value for key, value in sorted(dictionary.items(), key=lambda item: item[1])}

def finishBullying(truckBehind, leader, oldPosition, newPosition):
    # Inform the Truck behind
    acknowledgement = bullyAcknowledgement(truckBehind, leader, newPosition)
    if not acknowledgement or not acknowledgement.status_code == 200:
        truck = TruckEntity.objects.get(ID)
        truck.backTruckAddress = None
        truck.save()
    
    # Inform the Convoy Microservice
    bullied = overwriteRegistration(oldPosition, newPosition)
    if bullied and bullied.status_code == 200:
        return True
    else:
        return False

class BullyAlgorithm(Thread):
    def __init__(self):
        Thread.__init__(self, daemon=True)
        self.success = False
        self.failed = False
        self.tries = 0
    
    def run(self):
        while not self.failed and not self.success:
            self.__bully__()

    def __bully__(self):
        registerRequest = registered()
        if registerRequest.status_code == 200:
            addresses = registerRequest.json()
            sortedAddresses = sort(addresses)
            frontTruck, position = self.__findPosition__(sortedAddresses)
            
            if frontTruck == ADDRESS_SELF and position == 1:
                self.__makeLeader__()
            elif frontTruck and position:
                self.__actualizePosition__()
        else:
            self.tries += 1

    def __findPosition__(self, addresses: dict):
        """@returns the address of the truck in front and the position of own truck"""
        currentFrontTruck = ADDRESS_SELF
        position = 1
        
        # Iterate till you find own address
        for position, address in addresses.items():
            if address == ADDRESS_SELF:
                return (currentFrontTruck, position)
            
            currentTruckRequest = pollRequest(address)
            if not currentTruckRequest or currentTruckRequest.status_code == 400:
                pass
            # Increment / update for every responding truck
            elif currentTruckRequest.status_code == 200:
                currentFrontTruck = address
                position += 1
        
        # In case of not reacting to own address
        self.failed = True
        return (None, None)

    def __makeLeader__(self):
        """Sets leader attributes, gives acknowledgement to truck in back and overwrites the own convoy service position"""
        truck = TruckEntity.objects.get(ID)

        # Caching the value for the overwrite
        oldPosition = truck.position
        truckBehind = truck.backTruckAddress

        truck.frontTruckAddress = None
        truck.position = 1
        truck.leadingTruckAddress = ADDRESS_SELF
        truck.save()

        # Close the bully chain
        success = finishBullying(truckBehind, ADDRESS_SELF, oldPosition, 1)

        if success:
            self.success = True
        else:
            self.tries += 1

    def __actualizePosition__(self, frontTruck):
        """Sets information of new truck in front and tells it to start polling"""
        truck = TruckEntity.objects.get(ID)
        truck.frontTruckAddress = frontTruck
        truck.save()

        # Tell the truck in front to start bullying
        bullyChain = startBullying()
        if not bullyChain or not bullyChain.status_code == 200:
            self.success = True
        else:
            self.tries += 1
        
    
    def __deleteTruckBehind__(self):
        truck = TruckEntity.objects.get(ID)
        truck.backTruckAddress = None
        truck.save()

        # Ende ... erstmal ... Im Anschluss wird dann von vorne nach hinten durchgegeben, welche Positionen der jeweilige Vordermann nun hat und wer der aktuelle leader ist

def bully():
    bully = BullyAlgorithm()
    bully.start()