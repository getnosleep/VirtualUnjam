from rest_framework import serializers
from . import models

class ConvoySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Convoy
        fields = [models.__all__]
