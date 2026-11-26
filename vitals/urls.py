from django.urls import path
from . import views

urlpatterns = [
    path('vitals/', views.get_latest_vitals),
    path('reset-alarm/', views.reset_alarm),
]