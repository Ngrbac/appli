from rest_framework import serializers
from django.contrib.auth.models import User
from openweather.serializers import CityListSerializer

class UserSerializer(serializers.ModelSerializer):
    weathercity_set = CityListSerializer(read_only=True, many=True)
    class Meta:
        model = User
        fields = ('email', 'username', 'weathercity_set',)
        
class UserCreateSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = ('email', 'username', 'password',)
        write_only_fields = ('password',)
        