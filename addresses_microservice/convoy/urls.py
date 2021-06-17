from django.urls import path
from .views import ConvoyViewSet

urlpatterns = [
    path('', ConvoyViewSet.as_view({
        'post': 'register',
        'get': 'data',
        'put': 'bully',
        'delete': 'flush',
    })),
]