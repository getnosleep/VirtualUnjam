"""[Docstring] Defines which api calls respective."""
from django.urls import path
from .views import Initializer, Monitor

urlpatterns = [
    path('needle', Initializer.as_view({
        'post': 'initializeHeartbeats',
        'delete': 'stopHeartbeats'
    })),
    path('monitor', Monitor.as_view({
        'get': 'monitorHeartbeats'
    })),
]