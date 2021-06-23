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
            'address',

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

            'leadingTruckAddress',
            'position',
            'polling',
            'broken',
        ]

class BullySerializer(serializers.ModelSerializer):
    """Serialization of Truck-Data for Pollings"""
    class Meta:
        model = TruckEntity
        fields = [
            'id',
            'address',
            
            'leadingTruckAddress',
            'frontTruckAddress',
            'backTruckAddress',
            'position',
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
