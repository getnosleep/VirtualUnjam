from django.db.models import fields
from rest_framework import serializers
from .models import TruckEntity

class TruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = TruckEntity
        fields = [
            'truckid',
            'address',
            'targetDistance',
            'currentDistance',
            'targetSpeed',
            'currentSpeed',
            'broken',
            'convoyLeader',
            'convoyPosition',
            'polling',
            'accelerating',
            'decelerating',
        ]
