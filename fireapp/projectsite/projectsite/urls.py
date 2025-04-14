from django.urls import path
from fire.views import (
    HomePageView, 
    ChartView, 
    PieCountbySeverity, 
    LineCountbyMonth,
    MultilineIncidentTop3Country, 
    MultipleBarbySeverity, 
    map_station,
    fire_incident_map,
    # Remove dashboard_chart if you're not using it
    FireStationListView,
    FireStationCreateView,
    FireStationUpdateView,
    IncidentListView, 
    IncidentCreateView, 
    IncidentUpdateView,
    LocationListView, 
    LocationCreateView, 
    LocationUpdateView,
    ConditionListView, 
    ConditionCreateView, 
    ConditionUpdateView,
    FiretruckListView, 
    FiretruckCreateView, 
    FiretruckUpdateView,
    FirefightersListView, 
    FirefightersCreateView, 
    FirefightersUpdateView,
    BoatListView, 
    BoatCreateView, 
    BoatUpdateView
)

urlpatterns = [
    # Main views
    path('', HomePageView.as_view(), name='home'),
    path('chart/', ChartView.as_view(), name='chart'),
    
    # Chart data APIs
    path('chart-data/severity', PieCountbySeverity, name='chart-data-severity'),
    path('chart-data/month', LineCountbyMonth, name='chart-data-month'),
    path('chart-data/top3country', MultilineIncidentTop3Country, name='chart-data-top3country'),
    path('chart-data/multiplebar', MultipleBarbySeverity, name='chart-data-multiplebar'),
    
    # Map views
    path('map-station/', map_station, name='map-station'),
    path('fire-incident-map/', fire_incident_map, name='fire-incident-map'),
    
    # Fire Station URLs
    path('stations/', FireStationListView.as_view(), name='station-list'),
    path('station/create/', FireStationCreateView.as_view(), name='station-create'),
    path('station/<int:pk>/update/', FireStationUpdateView.as_view(), name='station-update'),
    
    # Incident URLs
    path('incidents/', IncidentListView.as_view(), name='incident-list'),
    path('incident/create/', IncidentCreateView.as_view(), name='incident-create'),
    path('incident/<int:pk>/update/', IncidentUpdateView.as_view(), name='incident-update'),
    
    # Location URLs
    path('locations/', LocationListView.as_view(), name='loc-list'),
    path('location/create/', LocationCreateView.as_view(), name='loc-create'),
    path('location/<int:pk>/update/', LocationUpdateView.as_view(), name='loc-update'),
    
    # Weather Condition URLs
    path('weather/', ConditionListView.as_view(), name='weather-list'),
    path('weather/create/', ConditionCreateView.as_view(), name='weather-create'),
    path('weather/<int:pk>/update/', ConditionUpdateView.as_view(), name='weather-update'),
    
    # Firetruck URLs
    path('firetrucks/', FiretruckListView.as_view(), name='fireTruck-list'),
    path('firetruck/create/', FiretruckCreateView.as_view(), name='fireTruck-create'),
    path('firetruck/<int:pk>/update/', FiretruckUpdateView.as_view(), name='fireTruck-update'),
    
    # Firefighters URLs
    path('firefighters/', FirefightersListView.as_view(), name='firefighters-list'),
    path('firefighter/create/', FirefightersCreateView.as_view(), name='firefighters-create'),
    path('firefighter/<int:pk>/update/', FirefightersUpdateView.as_view(), name='firefighters-update'),
    
    # Boat URLs
    path('boats/', BoatListView.as_view(), name='boat-list'),
    path('boat/create/', BoatCreateView.as_view(), name='boat-create'),
    path('boat/<int:pk>/update/', BoatUpdateView.as_view(), name='boat-update'),
]