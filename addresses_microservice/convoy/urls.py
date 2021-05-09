from django.urls import path
from .views import ConvoyViewSet

urlpatterns = [
    path('', ConvoyViewSet.as_view({
        'get': 'data', # alle Daten -> Komplettes Dictionary { truckId: address }
        'post': 'register', # registriere einen Truck { "truckId": int, "address": str }
        'delete': 'leave', # { truckId: int }
    })),
    path('trucks', ConvoyViewSet.as_view({
        'get': 'truckIds', # alle registrierten Truck IDs
    })),
    path('address:id', ConvoyViewSet.as_view({
        'get': 'address', # spezifische Adresse zu einer Truck ID
    })),
]