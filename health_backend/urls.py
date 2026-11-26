from django.contrib import admin
from django.urls import path
from vitals import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/vitals/', views.get_latest_vitals),
    path('api/reset-alarm/', views.reset_alarm),
]