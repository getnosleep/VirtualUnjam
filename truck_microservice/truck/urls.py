# imports
from django.urls import path
from .views import TruckBehaviour
from .views import TruckMonitoring
from .query import Query
from .initializer import Initializer

urlpatterns = [
    # Initialization
    path('init', Initializer.as_view({
        'post': 'truck'
    })),

    # Queries
    path('monitor', Query.as_view({
        'get': 'truck'
    })),
    path('monitor/settings', Query.as_view({
        'get': 'settings'
    })),
    path('monitor/status', Query.as_view({
        'get': 'status'
    })),
    path('monitor/actions', Query.as_view({
        'get': 'actions'
    })),

    # Mutations
    path('convoy', TruckBehaviour.as_view({
        'put': 'updateConvoy',
        'post': 'joinConvoy',
        'delete': 'leaveConvoy',
    })),
    path('accelerate', TruckBehaviour.as_view({
        'put': 'accelerate',
    })),
    path('decelerate', TruckBehaviour.as_view({
        'put': 'decelerate',
    })),
    path('stop', TruckBehaviour.as_view({
        'put': 'stop',
    }))
]
