"""[Docstring] Declares trucks' model."""
# Imports
from django.db import models
# Declare models as held in array.
__all__ = []
# Truck model class.
class Truck(object):
    """[Docstring] Declares truck model's properties and their data types.

    Properties: id = Primary_key, truckId = Integer, convoyPosition = Integer, convoyLeaderId = Integer, maxSpeed = Float, speed = Float.
    """
    
    # Declare truck model's properties and datatypes.
    id = models.AutoField(primary_key=True)
    truckId = models.IntegerField()
    convoyPosition = models.IntegerField()
    convoyLeaderId = models.IntegerField()
    maxSpeed = models.IntegerField()
    speed = models.FloatField()
    #truck_in_front = models.OneToOneField()
    #truck_behind = models.OneToOneField()
