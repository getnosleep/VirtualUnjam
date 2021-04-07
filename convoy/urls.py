# imports
from django.urls import path
from .views import ConvoyViewSet

urlpatterns = [
    path('convoyalive', ConvoyViewSet.as_view({
        'get': 'alive',
    })),
]
