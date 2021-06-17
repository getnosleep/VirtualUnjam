# library imports
from threading import Thread
from rest_framework.parsers import JSONParser
import time

# property imports
from ..properties import ID, ADDRESS_SELF, ADDRESS_CONVOY

# persistence layer imports
from ..models import TruckEntity

# extern requests
from ..extern_api.addresses import registered
from ..extern_api.trucks import convoyRequest

class BullyAlgorithm(Thread):
    def __init__(self):
        Thread.__init__(self, daemon=True)
    
    def run(self):
        self.requests()
    
    def requests(self):
        print('Funktioniert nicht, neu machen')
        return False
