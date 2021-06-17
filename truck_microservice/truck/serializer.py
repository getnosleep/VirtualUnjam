# library imports
from rest_framework import serializers

# persistence layer imports
from .models import TruckEntity

class AdminSerializer(serializers.ModelSerializer):
    """Serialization of Truck-Data for the Admin-Microservice"""
    class Meta:
        model = TruckEntity
        fields = [
            'position',
            'id',
            'length',

            'broken',
            'polling',
            'closing',
            'accelerating',
            'decelerating',

            'currentSpeed',
            'currentDistance',
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
            'distance',

            'currentDistance',
            'currentRouteSection',
            'currentSpeed',
            'acceleration',
            'targetRouteSection',
            'targetSpeed',

            'position',
            'polling',
            'broken',
        ]

class Serializer(serializers.ModelSerializer):
    """All Truck-Data serialization -> only for development purpose"""
    class Meta:
        model = TruckEntity
        fields = [
            # About this truck
            'id',
            'address',
            'length',
            'distance',

            # Movement
            'currentDistance',
            'currentRouteSection',
            'currentSpeed',
            'acceleration',
            'targetRouteSection',
            'targetSpeed',

            # Convoy
            'leadingTruckAddress',
            'frontTruckAddress',
            'backTruckAddress',
            'position',
            'polling',
            'broken',

            # Computed
            'closing',
            'accelerating',
            'decelerating',

            # Properties
            'minSpeed',
            'maxSpeed',
            'minAcceleration',
            'maxAcceleration',
        ]
