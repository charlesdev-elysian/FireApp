from django.urls import path
from .views import (
    HomePageView,
    ChartView,
    DashboardChartView,
    PieCountbySeverity,
    LineCountbyMonth,
    MultilineIncidentTop3Country,
    MultipleBarbySeverity,
    map_station,
    fire_incident_map,
    # Fire Station Views
    FireStationListView,
    FireStationCreateView,
    FireStationUpdateView,
    FireStationDeleteView,
    # Incident Views
    IncidentListView,
    IncidentCreateView,
    IncidentUpdateView,
    IncidentDeleteView,
    # Location Views
    LocationListView,
    LocationCreateView,
    LocationUpdateView,
    LocationDeleteView,
    # Weather Condition Views
    ConditionListView,
    ConditionCreateView,
    ConditionUpdateView,
    ConditionDeleteView,
    # Firetruck Views
    FiretruckListView,
    FiretruckCreateView,
    FiretruckUpdateView,
    FiretruckDeleteView,
    # Firefighter Views
    FirefightersListView,
    FirefightersCreateView,
    FirefightersUpdateView,
    FirefightersDeleteView
)

app_name = 'fire'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    
    # Chart URLs
    path('dashboard_chart', ChartView.as_view(), name='dashboard-chart'),
    path('dashboard_chart/', DashboardChartView.as_view(), name='dashboard-chart'),
    path('chart/', PieCountbySeverity, name='chart'),
    path('lineChart/', LineCountbyMonth, name='chart'),
    path('multilineChart/', MultilineIncidentTop3Country, name='chart'),
    path('multipleBarChart/', MultipleBarbySeverity, name='chart'),
    
    # Map URLs
    path('station/', map_station, name='map-station'),
    path('fire_incident_map/', fire_incident_map, name='fire-incident-map'),
    
    # Fire Station URLs
    path('firestation_list/', FireStationListView.as_view(), name='station-list'),
    path('firestation_list/add/', FireStationCreateView.as_view(), name='firestation-add'),
    path('firestation_list/<pk>/', FireStationUpdateView.as_view(), name='firestation-update'),
    path('firestation_list/<pk>/delete/', FireStationDeleteView.as_view(), name='firestation-delete'),
    
    #  # Incidents
    path('incident_list/', IncidentListView.as_view(), name='incident-list'),
    path('incident_list/add', IncidentCreateView.as_view(), name='incident-add'),
    path('incident_list/<pk>', IncidentUpdateView.as_view(), name='incident-update'),
    path('incident_list/<pk>/delete/', IncidentDeleteView.as_view(), name='incident-delete'),

    # Locations
    path('location_list/', LocationListView.as_view(), name='loc-list'),
    path('location_list/add', LocationCreateView.as_view(), name='location-add'),
    path('location_list/<pk>', LocationUpdateView.as_view(), name='location-update'),
    path('location_list/<pk>/delete/', LocationDeleteView.as_view(), name='location-delete'),

    # Conditions
    path('condition_list/', ConditionListView.as_view(), name='weather-list'),
    path('condition_list/add', ConditionCreateView.as_view(), name='condition-add'),
    path('condition_list/<pk>', ConditionUpdateView.as_view(), name='condition-update'),
    path('condition_list/<pk>/delete/', ConditionDeleteView.as_view(), name='condition-delete'),

    # Firetrucks
    path('firetruck_list/', FiretruckListView.as_view(), name='fireTruck-list'),
    path('firetruck_list/add', FiretruckCreateView.as_view(), name='firetruck-add'),
    path('firetruck_list/<pk>', FiretruckUpdateView.as_view(), name='firetruck-update'),
    path('firetruck_list/<pk>/delete/', FiretruckDeleteView.as_view(), name='firetruck-delete'),

    # Firefighters
    path('firefighters/', FirefightersListView.as_view(), name='firefighters-list'),
    path('firefighters/add/', FirefightersCreateView.as_view(), name='firefighters-add'),
    path('firefighters/<int:pk>/edit/', FirefightersUpdateView.as_view(), name='firefighters-update'),
    path('firefighters/<int:pk>/delete/', FirefightersDeleteView.as_view(), name='firefighters-delete'),
]