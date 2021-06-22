# library imports
from django.urls import path

# viewset imports
from .initializer import Initializer
from .query import Query
from .mutation import Mutation

urlpatterns = [
    # For Development purpose only !!!
    path('05FD548CB946F6AEFD3831FE4F1FD046E1827757E07F877F3A087B0ED98A03BF', Initializer.as_view({
        'get': 'truck',
        'post': 'init',
    })),

    # Queries
    path('truck', Query.as_view({
        'get': 'truckRequests',
    })),
    path('monitor', Query.as_view({
        'get': 'adminRequests',
    })),
    path('poll', Query.as_view({
        'get': 'pollRequests',
    })),

    # Mutations
    path('convoy', Mutation.as_view({
        'post': 'joinConvoy', # ADMIN
        'put': 'joinBehind',
        'delete': 'leaveConvoy', # ADMIN
    })),
    path('intact', Mutation.as_view({
        'post': 'repair', # ADMIN
        'delete': 'destroy', # ADMIN
    })),
    path('accelerate', Mutation.as_view({
        'post': 'accelerate', # ADMIN
    })),
    path('bully', Mutation.as_view({
        'post': 'startBullying',
        'put': 'updateAfterBullying',
    })),
    path('test', Mutation.as_view({
        'get': 'checkRequestTimes', # just dirty shit
    }))
]
