"""
[Docstring] Connects http request url to respective generic view.

Not not of any use yet. Can be included in main url.py.
"""
# imports
from django.urls import path
from . import views
# intitiate path prefix
app_name = 'api'
# intitiate url patterns
urlpatterns = [
    #path('', views.IndexView.as_view(), name='index'),
    #path('controller/<int:pk>/', views.ControllerIndexView.as_view(), name='controllers_list'),
    #path('<int:question_id>/votes/', views.vote, name='vote'),
]