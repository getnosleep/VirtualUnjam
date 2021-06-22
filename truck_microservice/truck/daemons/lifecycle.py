# library imports
from threading import Thread
from ..serializer import ConvoySerializer
from rest_framework.parsers import JSONParser

# property imports
from ..properties import ID

# persistence layer imports
from ..models import TruckEntity

# extern requests
from ..extern_api.trucks import convoyRequest
from .bully import BullyAlgorithm

class Lifecycle(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        self.__convoyUpdate__()
        self.__pollingCheck__()

    def __requestTruck__(self, trucksAddress):
        try:
            otherTruck = convoyRequest(trucksAddress)
            if otherTruck.status_code == 200:
                truck = JSONParser().parse(otherTruck)
                if truck['position']:
                    return truck
        except:
            pass
        return False

    def __accessTruckBehind__(self, backTruck):
        truckBehind = self.__requestTruck__(backTruck)
        if not truckBehind:
            truck = TruckEntity.objects.get(pk=ID)
            truck.backTruckAddress = None
            truck.save()

    def __accessTruckInFront__(self, frontTruck):
        truckInFront = self.__requestTruck__(frontTruck)
        if truckInFront:
            serialized = ConvoySerializer(data=truckInFront)
            if serialized.is_valid():
                serialized.save()
        else:
            truck = TruckEntity.objects.get(pk=ID)
            TruckEntity.objects.filter(address=truck.frontTruckAddress).delete()
            truck.frontTruckAddress = None
            truck.polling = True
            truck.save()


    def __convoyUpdate__(self):
        truck = TruckEntity.objects.get(pk=ID)

        frontTruck = truck.frontTruckAddress
        backTruck = truck.backTruckAddress

        leader = not frontTruck and backTruck
        lonely = not (frontTruck or backTruck)

        if lonely:
            print('I am so lonely')
            pass
        elif leader:
            # No thread needed
            print('I am the leader')
            self.__accessTruckBehind__(backTruck)
        else:
            # Here we need Threads
            print('I need instructions what to do')
            behind = Thread(self.__accessTruckBehind__(backTruck))
            front = Thread(self.__accessTruckInFront__(frontTruck))

            behind.join()
            front.join()
            pass

    def __pollingCheck__(self):
        polling = False

        # truck.polling -> muss nur eine Flanke sein ...

        if polling:
            BullyAlgorithm()
            # truck.polling = False -> Flanke zurueckgesetzt
            # ggf. sollte man die Flanke auch anders abfragen... ich ueberleg mir was elegantes
        pass

def alive():
    lifecycle = Lifecycle()
    lifecycle.start()
