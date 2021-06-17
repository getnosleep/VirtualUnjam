from django.urls import path
from .views import ConvoyViewSet

urlpatterns = [
    path('', ConvoyViewSet.as_view({
        'get': 'data',
        'post': 'register',
    })),
]