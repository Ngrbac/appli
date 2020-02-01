from django.contrib import admin
from .models import WeatherCity

# Omogućuje pregledavanje gradova na /admin dashboardu.

admin.site.register(WeatherCity)
