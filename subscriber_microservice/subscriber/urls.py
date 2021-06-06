"""[Docstring] Defines which api calls respective."""
from django.urls import path
from .views import Initializer, Monitor

urlpatterns = [
    # Initialization
    path('init', Initializer.as_view({
        'post': 'initializeSubscription',
        'delete': 'stopSubscription'
    })),

    # Queries
    path('monitor', Monitor.as_view({
        'get': 'monitorHeartbeats'
    }))
    
    # No mutations needed.
]