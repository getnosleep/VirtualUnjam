"""[Docstring] Declares model objects."""
# Imports
from django.db import models
# Truck model objects class
class Truck(object):
    """[Docstring] Declares model objects

    Properties:
    
        id Primary_key - UUID - Primary key for database,
        
        truckId Integer - unique id for distributed system,
        
        convoyPosition Integer - position in distributed Convoy,
        
        convoyLeaderId Integer - leader in distributed Convoy,
        
        maxSpeed Float - terminal velocity speed of the truck,
        
        speed Float - current speed of the truck.
    """

    # binding fields for serializers
    __all__ = [ "id", "truckId", "convoyPosition", "convoyLeaderId", "maxSpeed", "speed"]

    id = models.AutoField(primary_key=True)
    truckId = models.IntegerField()
    convoyPosition = models.IntegerField()
    convoyLeaderId = models.IntegerField()
    maxSpeed = models.FloatField()
    speed = models.FloatField()
    #truck_in_front = models.OneToOneField()
    #truck_behind = models.OneToOneField()
