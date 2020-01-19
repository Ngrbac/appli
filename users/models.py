from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from openweather.models import WeatherCity

# class User(AbstractUser):    
#     fav_cities = models.ManyToManyField(WeatherCity, blank=True)