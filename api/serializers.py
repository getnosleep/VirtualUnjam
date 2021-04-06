"""[Docstring] Declares serializers."""
# Imports
from rest_framework import serializers
from . import models
# Truck serializer class
class TruckSerializer(serializers.HyperlinkedModelSerializer):
    """[Docstring] Declares truck model serializer."""

    class Meta:
        """[Docstring] Declares truck model serializer's json structure."""

        model = models.Truck
        fields = ['truck_id', 'truck_convoy_id', 'truck_convoy_position', 'tour_id', 'start_time', 'driving_time',  'arrival_time', 'street_id', 'in_convoy', 'driving', 'stopped', 'in_depot', 'on_tour']
