"""[Docstring] Defines which api calls respective."""
from django.urls import path
from .views import Initializer, Monitor


urlpatterns = [
    # Initialization
    path('needle', Initializer.as_view({
        'post': 'initializeHeartbeats',
        'delete': 'stopHeartbeats'
    })),

    # Queries
    path('monitor', Monitor.as_view({
        'get': 'monitorHeartbeats'
    }))

    # No mutations needed.
]