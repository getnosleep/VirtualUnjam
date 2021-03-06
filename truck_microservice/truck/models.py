# library imports
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# property imports
from .properties import *

class TruckEntity(models.Model):
    # Params
    id = models.PositiveIntegerField(default=ID, primary_key=True)
    address = models.TextField(default=ADDRESS_SELF, max_length=50)
    length = models.FloatField(default=LENGTH)
    distance = models.FloatField(default=DISTANCE)

    # Movement
    currentDistance = models.FloatField(default=.0)
    currentRouteSection = models.FloatField(default=.0, validators=[MinValueValidator(.0)])
    currentSpeed = models.FloatField(default=.0, validators=[MinValueValidator(MIN_SPEED), MaxValueValidator(MAX_SPEED)])
    acceleration = models.FloatField(default=.0, validators=[MinValueValidator(MIN_ACCELERATION), MaxValueValidator(MAX_ACCELERATION)])
    targetRouteSection = models.FloatField(default=20000.0, validators=[MinValueValidator(.0)])
    targetSpeed = models.FloatField(default=.0, validators=[MinValueValidator(MIN_SPEED), MaxValueValidator(MAX_SPEED)])
    
    # Convoy
    leadingTruckAddress = models.TextField(default=None, blank=True, null=True, max_length=50)
    frontTruckAddress = models.TextField(default=None, blank=True, null=True, max_length=50)
    backTruckAddress = models.TextField(default=None, blank=True, null=True, max_length=50)
    position = models.PositiveIntegerField(default=None, blank=True, null=True)
    polling = models.BooleanField(default=False)
    broken = models.BooleanField(default=False)

    # Computed
    def closing(self):
        return self.distance > self.currentDistance and self.position and not self.leadingTruckAddress == ADDRESS_SELF

    def accelerating(self):
        return self.acceleration > .0

    def decelerating(self):
        return self.acceleration < .0

    def movementStats(self):
        return [self.currentRouteSection, self.currentSpeed, self.acceleration]
    
    def targetStats(self):
        return [self.targetRouteSection, self.targetSpeed]

    @property
    def minSpeed(self):
        return MIN_SPEED
    
    @property
    def maxSpeed(self):
        return MAX_SPEED
    
    @property
    def minAcceleration(self):
        return MIN_ACCELERATION
    
    @property
    def maxAcceleration(self):
        return MAX_ACCELERATION

# import socket # Koennte die richtige Loesung sein...
