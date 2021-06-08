# library imports
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# property imports
from .properties import ID, ADDRESS, LENGTH, MIN_SPEED, MAX_SPEED, MIN_ACCELERATION, MAX_ACCELERATION

class TruckEntity(models.Model):
    # Params
    id = models.PositiveIntegerField(default=ID, primary_key=True)
    address = models.CharField(default=ADDRESS, max_length=50)
    length = models.FloatField(default=LENGTH, validators=[MinValueValidator(0.0)])

    # Movement
    currentRouteSection = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    currentSpeed = models.FloatField(default=0.0, validators=[MinValueValidator(MIN_SPEED), MaxValueValidator(MAX_SPEED)])
    currentAcceleration = models.FloatField(default=0.0, validators=[MinValueValidator(MIN_ACCELERATION), MaxValueValidator(MAX_ACCELERATION)])
    targetRouteSection = models.FloatField(default=20000.0, validators=[MinValueValidator(0.0)])
    targetSpeed = models.FloatField(default=0.0, validators=[MinValueValidator(MIN_SPEED), MaxValueValidator(MAX_SPEED)])
    
    # Convoy
    polling = models.BooleanField(default=False)
    broken = models.BooleanField(default=False)
    convoyLeader = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    convoyPosition = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    # Computed
    def accelerating(self):
        return self.currentAcceleration > 0.0

    def decelerating(self):
        return self.currentAcceleration < 0.0

    def movementStats(self):
        return [self.currentRouteSection, self.currentSpeed, self.currentAcceleration]
    
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
