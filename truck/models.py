from django.db import models

# binding fields for serializers
__all__ = [ "id", "truckId", "convoyPosition", "convoyLeaderId", "maxSpeed", "speed"]

class Truck(models.Model):
    """[Docstring] Declares model objects.

    Properties:
    
        id Primary_key - UUID - Primary key for database,
        
        truckId Integer - unique id for distributed system,
        
        convoyPosition Integer - position in distributed Convoy,
        
        convoyLeaderId Integer - leader in distributed Convoy,
        
        speed Float - current speed of the truck.
    """
    
    id = models.AutoField(primary_key=True)
    truckId = models.IntegerField()
    convoyPosition = models.IntegerField()
    convoyLeaderId = models.IntegerField()
    speed = models.FloatField()
    #truck_in_front = models.OneToOneField()
    #truck_behind = models.OneToOneField()
