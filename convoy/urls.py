# imports
from django.urls import path
from .views import ConvoyViewSet

urlpatterns = [
    path('alive', ConvoyViewSet.as_view({
        'get': 'alive',
    })),
]
