"""[Docstring] Defines which api calls respective."""
from django.urls import path

from .views import Monitor

urlpatterns = [
    # Initialization

    # Queries
    path('test', Monitor.as_view({
        'get': 'test'
    })),

    path('test2', Monitor.as_view({
        'get': 'test2'
    })),

    path('runtest', Monitor.as_view({
        'get': 'runtest'
    })),

    path('datastacker', Monitor.as_view({
        'post': 'datastacker'
    }))

]