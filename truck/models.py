# from django.db import models

__all__ = []

class Truck(object):
    def __init__(self, id: int, speed: float, length: float, distance: float, optimal_distance: float, fleet: list):
        self.id = id
        self.speed = speed
        self.length = length
        self.distance = distance
        self.optimal_distance = optimal_distance
        self.truck_in_front = 2
        self.truck_behind = 2

