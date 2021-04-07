from django.db import models

# binding fields for serializers
__all__ = ["id", "truckId", "convoyPosition", "convoyLeaderId", "maxSpeed", "speed"]

class Truck(object):
    """
    Properties:\n
    id Primary_key - UUID - Primary key for database\n
    truckId Integer - unique id for distributed system\n
    convoyPosition Integer - position in distributed Convoy\n
    convoyLeaderId Integer - leader in distributed Convoy\n
    speed Float - current speed of the truck\n
    """

    id = models.AutoField(primary_key=True)
    truckId = models.IntegerField()
    convoyPosition = models.IntegerField()
    convoyLeaderId = models.IntegerField()
    speed = models.FloatField()
    #truck_in_front = models.OneToOneField()
    #truck_behind = models.OneToOneField()
