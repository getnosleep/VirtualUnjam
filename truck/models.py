"""[Docstring] Declares model objects."""
from django.db import models

# binding fields for serializers
__all__ = ["id", "truckId", "convoyPosition", "convoyLeaderId", "speed",
           "address", "isBroken", "isPolling", "isDecelerating", "isAccelerating"]

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
    truckId = models.IntegerField(default=0)
    convoyPosition = models.IntegerField(default=None)
    convoyLeaderId = models.IntegerField(default=None)
    speed = models.FloatField(default=0)
    address = models.TextField(default='127.0.0.1:8000')
    isBroken = models.BooleanField(default=False)
    isPolling = models.BooleanField(default=False)
    isDecelerating = models.BooleanField(default=False)
    isAccelerating = models.BooleanField(default=False)
