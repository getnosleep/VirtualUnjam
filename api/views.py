"""[Docstring] Views for app entry points."""
# Imports
from rest_framework import viewsets
from rest_framework import permissions
from . import serializers
from . import models
# Trucks view set class.
class TruckViewSet(viewsets.ModelViewSet):
    """[Docstring] Declares truck model's view set."""

    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = models.Truck.objects.all().order_by('-truck_id')
    serializer_class = serializers.TruckSerializer
    permission_classes = [permissions.IsAuthenticated]
