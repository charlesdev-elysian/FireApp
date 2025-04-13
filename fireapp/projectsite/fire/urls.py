# fire/urls.py
from django.urls import path
from . import views

app_name = 'fire'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('dashboard_chart/', views.ChartView.as_view(), name='dashboard-chart'),

    # Charts
    path('chart/', views.PieCountbySeverity, name='chart'),
    path('lineChart/', views.LineCountbyMonth, name='line-chart'),
    path('multiLineIncidentTop3Country/', views.MultilineIncidentTop3Country, name='multiline-incident-country'),
    path('multipleBarbySeverity/', views.multipleBarbySeverity, name='multiple-bar-severity'),

    # Map views
    path('map_station/', views.map_station, name='map-station'),
    path('incident_map/', views.fire_incident_map, name='fire-incident-map'),

    # ... (other CRUD views for incidents, locations, etc.)
]
