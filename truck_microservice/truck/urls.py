# library imports
from django.urls import path

# viewset imports
from .initializer import Initializer
from .query import Query
from .mutation import Mutation

urlpatterns = [
    # For Development purpose only !!!
    path('05FD548CB946F6AEFD3831FE4F1FD046E1827757E07F877F3A087B0ED98A03BF', Initializer.as_view({
        'get': 'truck',
        'post': 'recommendedInit',
        'put': 'specificInit',
    })),

    # Queries
    path('convoy', Query.as_view({
        'get': 'convoyRequests',
    })),
    path('monitor', Query.as_view({
        'get': 'adminRequests',
    })),

    # Mutations
    path('convoy', Mutation.as_view({
        'post': 'joinConvoy',
        'put': 'emergencyBrake',
        'delete': 'leaveConvoy',
    })),
    path('accelerate', Mutation.as_view({
        'post': 'accelerate',
    })),
    path('decelerate', Mutation.as_view({
        'post': 'decelerate',
    })),
]
