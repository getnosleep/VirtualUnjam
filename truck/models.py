from django.db import models

__all__ = []

class Truck(object):
    id = models.AutoField(primary_key=True)
    truck_identificator = models.TextField()
    convoy_position = models.IntegerField()
    leader_convoy_position = models.IntegerField()
    speed = models.FloatField()
    #truck_in_front = models.OneToOneField()
    #truck_behind = models.OneToOneField()
