from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('weather-summary/', views.weather_summary_api, name='weather_summary'),
]