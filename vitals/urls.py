
from django.urls import path
from . import views

urlpatterns = [
    path('devices/', views.list_devices),
    path('toggle/', views.toggle_device),
]