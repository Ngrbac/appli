from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class WeatherCity(models.Model):
    name = models.CharField(max_length=100)    
    featured = models.BooleanField(default=False)
    favourite = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    api_id = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
    