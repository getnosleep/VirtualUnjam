"""[Docstring] Defines which api calls respective."""
from django.urls import path

from .views import Mutation, Monitor

urlpatterns = [
    # Initialization

    # Queries
    path('activeTrucks', Monitor.as_view({
        'get': 'truckAdresses',
    })),

    path('convoy', Monitor.as_view({
        'post': 'activate',
        'delete': 'deactivate',
    })),

    path('monitor', Monitor.as_view({
        'get': 'dataStacker',
    })),
    path('web', Monitor.as_view({
        'get': 'web',
    })),

    # Mutations
    path('convoy', Mutation.as_view({
        'post': 'joinConvoy', # ADMIN
        'delete': 'leaveConvoy', # ADMIN
    })),
    path('intact', Mutation.as_view({
        'post': 'repair', # ADMIN
        'delete': 'destroy', # ADMIN
    })),
    path('accelerate', Mutation.as_view({
        'post': 'accelerate', # ADMIN
    })),
    path('inject', Mutation.as_view({
        'post': 'inject', # ADMIN
    }))

]