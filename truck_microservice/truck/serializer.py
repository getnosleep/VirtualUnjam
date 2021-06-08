# library imports
from django.db.models import fields
from rest_framework import serializers

# persistence layer imports
from .models import TruckEntity

class AdminSerializer(serializers.ModelSerializer):
    """Serialization of Truck-Data for the Admin-Microservice"""
    class Meta:
        model = TruckEntity
        fields = [
            'convoyPosition',
            'id',
            'length',
            'broken',

            'polling',
            'accelerating',
            'decelerating',
            'currentSpeed',
            'currentRouteSection',
            'targetRouteSection',
        ]

class ConvoySerializer(serializers.ModelSerializer):
    """Serialization of Truck-Data for other Truck-Microservice"""
    class Meta:
        model = TruckEntity
        fields = [
            'id',
            'address',
            'length',

            'currentRouteSection',
            'currentSpeed',
            'currentAcceleration',
            'targetRouteSection',
            'targetSpeed',

            'minSpeed',
            'maxSpeed',
            'minAcceleration',
            'maxAcceleration',
        ]

class Serializer(serializers.ModelSerializer):
    """All Truck-Data serialization -> only for development purpose"""
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
