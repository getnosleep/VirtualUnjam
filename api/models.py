"""[Docstring] Declares api's object models."""
# Imports
from django.db import models
# Create your models here.
class Truck(models.Model):
    """[Docstring] Declares truck model's fields."""

    truck_id = models.AutoField(primary_key=True)
    truck_convoy_id = models.IntegerField()
    truck_convoy_position = models.IntegerField()
    tour_id = models.IntegerField()
    start_time = models.DateTimeField('started driving')
    driving_time = models.IntegerField()
    arrival_time = models.DateTimeField('arrival driving')
    street_id = models.IntegerField()
    in_convoy = models.BooleanField(default=False)
    driving = models.BooleanField(default=False)
    stopped = models.BooleanField(default=True)
    in_depot = models.BooleanField(default=True)
    on_tour = models.BooleanField(default=False)
"""
class TruckConvoy(models.Model):
    truck_convoy_id = models.AutoField(primary_key=True)
    number_of_trucks_in_convoy = models.IntegerField()
    convoy_destination_id = models.IntegerField()
    convoy_departure_id = models.IntegerField()
    trucks = models.ManyToManyField(models.ForeignKey(Truck, on_delete=models.CASCADE), verbose_name="list of trucks")
class Tour(models.Model):
    tour_id = models.AutoField(primary_key=True)
    departure_point_id = models.IntegerField()
    destionation_id = models.IntegerField()
    trucks = models.ManyToManyField(models.ForeignKey(Truck, on_delete=models.CASCADE), verbose_name="list of trucks")
class Street(models.Model):
    street_id = models.AutoField(primary_key=True)
    position_x = models.IntegerField()
    position_y = models.IntegerField()
    neighbours = models.ManyToManyField(models.IntegerField(), verbose_name="list of neighbours")
class StreetGrid(models.Model):
    street_grid_id = models.AutoField(primary_key=True)
    size_x = models.IntegerField()
    size_y = models.IntegerField()
    streets = models.ManyToManyField(models.ForeignKey(Street, on_delete=models.CASCADE), verbose_name="list of streets")
class Depot(models.Model):
    depot_id = models.AutoField(primary_key=True)
    position_x = models.IntegerField()
    position_y = models.IntegerField()
class DepotGrid(models.Model):
    depot_grid_id = models.AutoField(primary_key=True)
    depots = models.ManyToManyField(models.ForeignKey(Depot, on_delete=models.CASCADE), verbose_name="list of destinations")
class Destination(models.Model):
    destination_id = models.AutoField(primary_key=True)
    position_x = models.IntegerField()
    position_y = models.IntegerField()
class DestinationGrid(models.Model):
    destination_grid_id = models.AutoField(primary_key=True)
    destinations = models.ManyToManyField(models.ForeignKey(Destination, on_delete=models.CASCADE), verbose_name="list of destinations")
class MapTile():
    tile_id = models.AutoField(primary_key=True)
    position_x = models.IntegerField()
    position_y = models.IntegerField()
class Map(models.Model):
    map_id = models.AutoField(primary_key=True)
    destination_grid = models.ForeignKey(DestinationGrid, on_delete=models.CASCADE)
    street_grid = models.ForeignKey(StreetGrid, on_delete=models.CASCADE)
    depot_grid = models.ForeignKey(DepotGrid, on_delete=models.CASCADE)
class SimulationValues(models.Model):
    breaking_chances = models.SmallIntegerField(0.001)
    number_of_destinations = models.IntegerField()
    number_of_depots = models.IntegerField()
    number_of_trucks_per_depot = models.IntegerField()
class Controller(models.Model):
    controller_id = models.AutoField(primary_key=True)
    maps = models.ManyToManyField(models.ForeignKey(Map, on_delete=models.CASCADE), verbose_name="list of destinations")
    simulationValues = models.ForeignKey(SimulationValues, on_delete=models.CASCADE)
"""