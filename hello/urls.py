from django.urls import path

from . import views

urlpatterns = [    
    path('', views.hello, name='hello'),
    path('filter', views.filter_this, name='filter'),
]
