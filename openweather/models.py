from django.db import models
from django.conf import settings

### Model za gradove.

# Featured atribut je za dodavanje fiksnih gradova sa strane.
# Favourite je za dodavanje omiljenih gradova. ManyToMany field spaja trenutnog korisnika i grad putem PK.

class WeatherCity(models.Model):
    name = models.CharField(max_length=100)    
    featured = models.BooleanField(default=False)
    favourite = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    api_id = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
    