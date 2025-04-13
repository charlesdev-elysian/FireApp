# projectsite/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('boats/', include('boats.urls')),  # <- this line requires boats/urls.py to exist
    path('', include('fire.urls')),         # This is your fire app main routing
]
