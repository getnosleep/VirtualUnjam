# imports
from django.urls import path
from .views import TruckViewSet

# intitiate path prefix
# app_name = 'api'
# intitiate url patterns

urlpatterns = [
    #    url-path, classview
    path('truck', TruckViewSet.as_view({
        # http request type: function from classview
        'get': 'retrieve',
        'put': 'update_fleet',
        'post': 'set_speed'
    })),
    path('liferequest', TruckViewSet.as_view({
        'get': 'alive'
    }))
]
