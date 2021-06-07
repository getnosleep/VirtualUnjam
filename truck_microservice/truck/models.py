from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from .properties import MIN_SPEED, MAX_SPEED, MIN_ACCELERATION, MAX_ACCELERATION

class TruckEntity(models.Model):
    # Params
    truckId = models.IntegerField(primary_key=True, validators=[MinValueValidator(1)])
    address = models.CharField(max_length=50)

    # Movement stats
    currentDistance = models.PositiveIntegerField(default=20, validators=[MinValueValidator(1)])
    currentSpeed = models.FloatField(validators=[MinValueValidator(MIN_SPEED), MaxValueValidator(MAX_SPEED)])
    currentAcceleration = models.FloatField(validators=[MinValueValidator(MIN_ACCELERATION), MaxValueValidator(MAX_ACCELERATION)])
    
    # Target stats
    targetDistance = models.PositiveIntegerField(default=20, validators=[MinValueValidator(1)])
    targetSpeed = models.FloatField(validators=[MinValueValidator(MIN_SPEED), MaxValueValidator(MAX_SPEED)])
    
    # Convoy stats
    broken = models.BooleanField(default=False)
    convoyLeader = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    convoyPosition = models.PositiveIntegerField(validators=[MinValueValidator(0)])

    # Computed stats
    def polling(self):
        return self.convoyLeader and not self.convoyPosition

    def accelerating(self):
        return self.targetSpeed > self.currentSpeed

    def decelerating(self):
        return self.targetSpeed < self.currentSpeed

    def movementStats(self):
        return [self.currentDistance, self.currentSpeed, self.currentAcceleration]
    
    def targetStats(self):
        return [self.targetDistance, self.targetSpeed]

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
