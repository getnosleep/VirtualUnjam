# imports
from django.urls import path
from .views import TruckBehaviour
from .views import TruckMonitoring

urlpatterns = [
    path('truck', TruckBehaviour.as_view({
        'get': 'alive',
        'post': 'create',
    })),
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
    })),
    path('data', TruckMonitoring.as_view({
        'get': 'retrieve',
    }))
]
