"""[Docstring] Defines which api calls respective."""
from django.urls import path

from .views import Mutation, Monitor

urlpatterns = [
    # Initialization

    # Queries
    path('web', Monitor.as_view({
        'get': 'web',
    })),

    # Mutations
    path('convoy', Mutation.as_view({
        'post': 'joinConvoy',
        'delete': 'leaveConvoy',
    })),
    path('intact', Mutation.as_view({
        'post': 'repair',
        'delete': 'destroy',
    })),
    path('accelerate', Mutation.as_view({
        'post': 'accelerate',
    })),
    path('inject', Mutation.as_view({
        'post': 'inject',
        'delete': 'flatline'
    }))

]