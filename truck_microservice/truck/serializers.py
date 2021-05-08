from rest_framework import serializers
from . import models

class TruckSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Truck
        fields = [models.__all__]
