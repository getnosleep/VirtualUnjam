# imports
from django.urls import path
from .query import Query
from .mutation import Mutation

urlpatterns = [
    # Queries
    path('monitor', Query.as_view({
        'get': 'truck'
    })),
    # path('monitor/settings', Query.as_view({
    #     'get': 'settings'
    # })),
    # path('monitor/status', Query.as_view({
    #     'get': 'status'
    # })),
    # path('monitor/actions', Query.as_view({
    #     'get': 'actions'
    # })),

    # Mutations
    path('convoy', Mutation.as_view({
        'put': 'emergencyBrake',
        'post': 'joinConvoy',
        'delete': 'leaveConvoy',
    })),
    path('accelerate', Mutation.as_view({
        'post': 'accelerate',
    })),
    path('decelerate', Mutation.as_view({
        'post': 'decelerate',
    })),
    path('initialize', Mutation.as_view({
        'post': 'selfInitialize'
    })),
]
