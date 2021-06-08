from django.db.models import fields
from rest_framework import serializers
from .models import TruckEntity

class AdminSerializer(serializers.ModelSerializer):
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
