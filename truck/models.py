from django.db import models

# binding fields for serializers
__all__ = [ "id", "truckId", "convoyPosition", "convoyLeaderId", "maxSpeed", "speed", "isBroken", "isPolling"]

class Truck(models.Model):
    """[Docstring] Declares model objects.

    Properties:
    
        id Primary_key - UUID - Primary key for database,
        
        truckId Integer - unique id for distributed system,
        
        convoyPosition Integer - position in distributed Convoy,
        
        convoyLeaderId Integer - leader in distributed Convoy,
        
        speed Float - current speed of the truck,

        isBroken Boolean - flags operational readiness of the truck,

        isPolling - flags polling status.
    """
    
    id = models.AutoField(primary_key=True)
    truckId = models.IntegerField()
    convoyPosition = models.IntegerField()
    convoyLeaderId = models.IntegerField()
    speed = models.FloatField()
    isBroken = models.BooleanField()
    isPolling = models.BooleanField()
    #truck_in_front = models.OneToOneField()
    #truck_behind = models.OneToOneField()
