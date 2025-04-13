from django.shortcuts import render
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.db.models import Q
from django.db import connection
from django.http import JsonResponse
from datetime import datetime

# Models
from .models import (
    Locations, 
    Incident, 
    FireStation, 
    WeatherConditions, 
    FireTruck, 
    Firefighters,
    Boat
)

# Forms
from .forms import (
    Loc_Form,
    Incident_Form,
    FireStationzForm,
    Weather_condition,
    Firetruckform,
    FirefightersForm
)

# ======================
# MAIN VIEWS
# ======================
class HomePageView(ListView):
    model = Locations
    context_object_name = 'home'
    template_name = "home.html"

class ChartView(TemplateView):
    template_name = 'chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class DashboardChartView(TemplateView):
    template_name = 'dashboard/chart.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Dashboard Charts"
        return context

# ======================
# CHART DATA VIEWS
# ======================
def PieCountbySeverity(request):
    query = '''
    SELECT severity_level, COUNT(*) as count
    FROM fire_incident
    GROUP BY severity_level
    '''
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    data = {severity: count for severity, count in rows} if rows else {}
    return JsonResponse(data)

def LineCountbyMonth(request):
    current_year = datetime.now().year
    result = {month: 0 for month in range(1, 13)}

    incidents = Incident.objects.filter(date_time__year=current_year).values_list('date_time', flat=True)
    for date_time in incidents:
        result[date_time.month] += 1

    month_names = {
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
        7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
    }

    return JsonResponse({month_names[month]: count for month, count in result.items()})

def MultilineIncidentTop3Country(request):
    query = '''
    SELECT 
        fl.country,
        strftime('%m', fi.date_time) AS month,
        COUNT(fi.id) AS incident_count
    FROM 
        fire_incident fi
    JOIN 
        fire_locations fl ON fi.location_id = fl.id
    WHERE 
        fl.country IN (
            SELECT 
                fl_top.country
            FROM 
                fire_incident fi_top
            JOIN 
                fire_locations fl_top ON fi_top.location_id = fl_top.id
            WHERE 
                strftime('%Y', fi_top.date_time) = strftime('%Y', 'now')
            GROUP BY 
                fl_top.country
            ORDER BY 
                COUNT(fi_top.id) DESC
            LIMIT 3
        )
        AND strftime('%Y', fi.date_time) = strftime('%Y', 'now')
    GROUP BY 
        fl.country, month
    ORDER BY 
        fl.country, month;
    '''

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    months = set(str(i).zfill(2) for i in range(1, 13))
    result = {}

    for country, month, count in rows:
        if country not in result:
            result[country] = {m: 0 for m in months}
        result[country][month] = count

    while len(result) < 3:
        result[f"Country {len(result) + 1}"] = {m: 0 for m in months}

    return JsonResponse({k: dict(sorted(v.items())) for k, v in result.items()})

def MultipleBarbySeverity(request):
    query = '''
    SELECT 
        fi.severity_level,
        strftime('%m', fi.date_time) AS month,
        COUNT(fi.id) AS incident_count
    FROM 
        fire_incident fi
    GROUP BY fi.severity_level, month
    '''

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    months = set(str(i).zfill(2) for i in range(1, 13))
    result = {}

    for level, month, count in rows:
        if level not in result:
            result[str(level)] = {m: 0 for m in months}
        result[str(level)][month] = count

    return JsonResponse({k: dict(sorted(v.items())) for k, v in result.items()})

# ======================
# MAP VIEWS
# ======================
def map_station(request):
    stations = FireStation.objects.values('name', 'latitude', 'longitude')
    stations = [{
        'name': s['name'],
        'latitude': float(s['latitude']),
        'longitude': float(s['longitude'])
    } for s in stations]

    return render(request, 'map_station.html', {'fireStations': stations})

def fire_incident_map(request):
    incidents = Locations.objects.values('name', 'latitude', 'longitude')
    incidents = [{
        'name': i['name'],
        'latitude': float(i['latitude']),
        'longitude': float(i['longitude'])
    } for i in incidents]

    return render(request, 'fire_incident_map.html', {'fireIncidents': incidents})

# ======================
# BASE CRUD VIEWS
# ======================
class BaseListView(ListView):
    paginate_by = 10
    context_object_name = 'object_list'
    
    def get_queryset(self):
        qs = super().get_queryset()
        if query := self.request.GET.get("q"):
            qs = qs.filter(self.get_search_filter(query))
        return qs
    
    def get_search_filter(self, query):
        return Q()

class BaseCreateView(CreateView):
    def form_valid(self, form):
        messages.success(self.request, f"{self.model._meta.verbose_name} created successfully!")
        return super().form_valid(form)

class BaseUpdateView(UpdateView):
    def form_valid(self, form):
        messages.success(self.request, f"{self.model._meta.verbose_name} updated successfully!")
        return super().form_valid(form)

class BaseDeleteView(DeleteView):
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, f"{self.model._meta.verbose_name} deleted successfully!")
        return super().delete(request, *args, **kwargs)

# ======================
# FIRE STATION VIEWS
# ======================
class FireStationListView(BaseListView):
    model = FireStation
    template_name = 'firestation/station_list.html'
    
    def get_search_filter(self, query):
        return (Q(name__icontains=query) | 
                Q(address__icontains=query) |
                Q(city__icontains=query) | 
                Q(country__icontains=query))

class FireStationCreateView(BaseCreateView):
    model = FireStation
    form_class = FireStationzForm
    template_name = 'firestation/station_form.html'
    success_url = reverse_lazy('station-list')

class FireStationUpdateView(BaseUpdateView):
    model = FireStation
    form_class = FireStationzForm
    template_name = 'firestation/station_form.html'
    success_url = reverse_lazy('station-list')

class FireStationDeleteView(BaseDeleteView):
    model = FireStation
    template_name = 'firestation/station_confirm_delete.html'
    success_url = reverse_lazy('station-list')
    
## Weather Condition Views
class ConditionListView(ListView):
    model = WeatherConditions
    context_object_name = 'object_list'
    template_name = 'weather_list.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super(ConditionListView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(incident__location__name__icontains=query) | 
                Q(temperature__icontains=query) |
                Q(humidity__icontains=query) |
                Q(wind_speed__icontains=query) |
                Q(weather_description__icontains=query)
            )
        return qs
    
class ConditionCreateView(CreateView):
    model = WeatherConditions
    form_class = Weather_condition
    template_name = 'weather_add.html'
    success_url = reverse_lazy('weather-list')

class ConditionUpdateView(UpdateView):
    model = WeatherConditions
    form_class = Weather_condition
    template_name = 'weather_edit.html'
    success_url = reverse_lazy('weather-list')

class ConditionDeleteView(DeleteView):
    model = WeatherConditions
    template_name = 'weather_del.html'
    success_url = reverse_lazy('weather-list')

## Firetruck Views
class FiretruckListView(ListView):
    model = FireTruck
    context_object_name = 'firetruck'
    template_name = 'firetruck_list.html'
    paginate_by = 10 
    
    
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(Q(truck_number__icontains=query) | 
            Q(model__icontains=query) | 
            Q(capacity__icontains=query) | 
            Q(station__name__icontains=query))

        return qs

class FiretruckCreateView(CreateView):
    model = FireTruck
    form_class = Firetruckform
    template_name = 'firetruck_add.html'
    success_url = reverse_lazy('fireTruck-list')

class FiretruckUpdateView(UpdateView):
    model = FireTruck
    form_class = Firetruckform
    template_name = 'firetruck_edit.html'
    success_url = reverse_lazy('fireTruck-list')

class FiretruckDeleteView(DeleteView):
    model =  FireTruck
    template_name = 'firetruck_del.html'
    success_url = reverse_lazy('fireTruck-list')
    
    
## Firefighter Views
class FirefightersListView(ListView):
    model = Firefighters
    context_object_name = 'firefighters'
    template_name = 'firefighter_list.html'
    paginate_by = 10 
    
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(Q(name__icontains=query))
        return qs

class FirefightersCreateView(CreateView):
    model = Firefighters
    form_class = FirefightersForm
    template_name = 'firefighter_add.html'
    success_url = reverse_lazy('firefighters-list')

class FirefightersUpdateView(UpdateView):
    model = Firefighters
    form_class = FirefightersForm
    template_name = 'firefighter_edit.html'
    success_url = reverse_lazy('firefighters-list')

class FirefightersDeleteView(DeleteView):
    model = Firefighters
    template_name = 'firefighter_del.html'
    success_url = reverse_lazy('firefighters-list')
    
## Boat Views  
class BoatCreateView(CreateView):
    model = Boat
    fields = "__all__"
    template_name = "boats/boat_form.html"
    success_url = reverse_lazy('boat-list')

    def validate_dimensions(self, data):
        """Centralized dimension validation logic"""
        errors = []
        for field in ['length', 'width', 'height']:
            value = data.get(field)
            try:
                if float(value) <= 0:
                    errors.append(f"{field.capitalize()} must be greater than 0.")
            except (ValueError, TypeError):
                errors.append(f"{field.capitalize()} must be a valid number.")
        return errors

    def form_valid(self, form):
        """Handle form validation with dimension checks"""
        errors = self.validate_dimensions(form.cleaned_data)
        if errors:
            for error in errors:
                messages.error(self.request, error)
            return self.form_invalid(form)
        
        messages.success(self.request, "Boat created successfully!")
        return super().form_valid(form)

class BoatUpdateView(UpdateView):
    model = Boat
    fields = "__all__"
    template_name = "boats/boat_form.html"
    success_url = reverse_lazy('boat-list')

    def validate_dimensions(self, data):
        """Reuse the same validation logic as CreateView"""
        errors = []
        for field in ['length', 'width', 'height']:
            value = data.get(field)
            try:
                if float(value) <= 0:
                    errors.append(f"{field.capitalize()} must be greater than 0.")
            except (ValueError, TypeError):
                errors.append(f"{field.capitalize()} must be a valid number.")
        return errors

    def form_valid(self, form):
        """Handle form validation with dimension checks"""
        errors = self.validate_dimensions(form.cleaned_data)
        if errors:
            for error in errors:
                messages.error(self.request, error)
            return self.form_invalid(form)
        
        messages.success(self.request, "Boat updated successfully!")
        return super().form_valid(form)
    
## Incident Views

class IncidentListView(ListView):
    model = Incident
    template_name = 'incidents/incident_list.html'
    context_object_name = 'incidents'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        
        if search_query:
            queryset = queryset.filter(
                Q(description__icontains=search_query) |
                Q(severity_level__icontains=search_query) |
                Q(location__name__icontains=search_query)
            )
        return queryset

class IncidentCreateView(CreateView):
    model = Incident
    form_class =  Incident_Form
    template_name= 'incident_add.html'
    success_url = reverse_lazy('incident-list')
    
class IncidentUpdateView(UpdateView):
    model = Incident
    form_class =  Incident_Form
    template_name= 'incident_edit.html'
    success_url = reverse_lazy('incident-list')
    
class IncidentDeleteView(DeleteView):
    model = Incident
    template_name= 'incident_del.html'
    success_url = reverse_lazy('incident-list')
    
class LocationListView(ListView):
    model = Locations
    template_name = 'loc_list.html'
    context_object_name = 'object_list'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(
                Q(name__icontains=query) |
                Q(address__icontains=query) |
                Q(city__icontains=query) |
                Q(country__icontains=query)
            )
        return qs
    
## Location Views
class LocationCreateView(CreateView):
    model = Locations
    form_class = Loc_Form
    template_name= 'loc_add.html'
    success_url = reverse_lazy('loc-list')
    
class LocationUpdateView(UpdateView):
    model = Locations
    form_class = Loc_Form
    template_name= 'loc_edit.html'
    success_url = reverse_lazy('loc-list')
    
class LocationDeleteView(DeleteView):
    model = Locations
    template_name= 'loc_del.html'
    success_url = reverse_lazy('loc-list')

class ConditionListView(ListView):
    model = WeatherConditions
    context_object_name = 'object_list'
    template_name = 'weather_list.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super(ConditionListView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(incident__location__name__icontains=query) | 
                Q(temperature__icontains=query) |
                Q(humidity__icontains=query) |
                Q(wind_speed__icontains=query) |
                Q(weather_description__icontains=query)
            )
        return qs
