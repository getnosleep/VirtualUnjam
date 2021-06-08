from django.db.models import fields
from rest_framework import serializers
from .models import TruckEntity

class TruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = TruckEntity
        fields = [
            # Params
            'id',
            'address',
            'length',

            # Movement
            'currentRouteSection',
            'currentSpeed',
            'currentAcceleration',
            'targetRouteSection',
            'targetSpeed',

            # Convoy
            'polling',
            'broken',
            'convoyLeader',
            'convoyPosition',

            # Computed
            'accelerating',
            'decelerating',

            # Properties
            'minSpeed',
            'maxSpeed',
            'minAcceleration',
            'maxAcceleration',
        ]
