from rest_framework import serializers
from .models import WeatherCity

class CityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherCity
        fields = ('name',)
        
class CityCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherCity
        fields = ('name',)

class WeatherElemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    main = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=100)
    icon = serializers.CharField(max_length=100)
    class Meta:
        fields = '__all__' #('id', 'main', 'description', 'icon')

class WeatherSerializer(serializers.Serializer):
    coord = serializers.DictField()
    weather = WeatherElemSerializer(many=True)
    base = serializers.CharField(max_length=100)
    main = serializers.DictField()
    visibility = serializers.IntegerField()
    wind = serializers.DictField()
    clouds = serializers.DictField()
    dt = serializers.IntegerField()
    sys = serializers.DictField()
    timezone = serializers.IntegerField()
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    cod = serializers.IntegerField()
    