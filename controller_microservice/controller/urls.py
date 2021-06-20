"""[Docstring] Defines which api calls respective."""
from django.urls import path

from .views import Monitor

urlpatterns = [
    # Initialization

    # Queries
    path('activeTrucks', Monitor.as_view({
        'get': 'truckAdresses',
    })),

    path('test2', Monitor.as_view({
        'get': 'test2',
    })),

    path('convoy', Monitor.as_view({
        'post': 'activate',
        'delete': 'deactivate',
    })),

    path('monitor', Monitor.as_view({
        'get': 'dataStacker',
    }))

]