"""[Docstring] Declares model objects."""
from django.db import models

# binding fields for serializers
__all__ = [ "id", "truckId", "convoyPosition", "convoyLeaderId", "speed", "address", "isBroken", "isPolling", "isBreaking", "isAccelerating"]

class Truck(models.Model):
    """[Docstring] Declares model objects.

    Properties:
    
        id Primary_key - UUID - Primary key for database,
        
        truckId Integer - unique id for distributed system,
        
        convoyPosition Integer - position in distributed Convoy,
        
        convoyLeaderId Integer - leader in distributed Convoy,
        
        speed Float - current speed of the truck,

        address Text - truck's microservice address,

        isBroken Boolean - flags operational readiness of the truck,

        isPolling - flags polling status,
        
        isDecelerating - flags breaking status,
        
        isAccelerating - flags acceleration status.
    """
    
    id = models.AutoField(primary_key=True)
    truckId = models.IntegerField()
    convoyPosition = models.IntegerField()
    convoyLeaderId = models.IntegerField()
    speed = models.FloatField()
    address = models.TextField()
    isBroken = models.BooleanField()
    isPolling = models.BooleanField()
    isDecelerating = models.BooleanField()
    isAccelerating = models.BooleanField()
