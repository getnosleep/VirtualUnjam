# imports
from django.urls import path
from .views import TruckBehaviour
from .views import TruckMonitoring

# intitiate path prefix
# app_name = 'api'
# intitiate url patterns

urlpatterns = [
    #    url-path, classview
    path('truck', TruckBehaviour.as_view({
        # http request type: function from classview
        'put': 'update_fleet',
        'post': 'set_speed'
    })),
    path('liferequest', TruckBehaviour.as_view({
        'get': 'alive'
    })),
    path('data', TruckMonitoring.as_view({
        'get': 'retrieve'
    }))
]
