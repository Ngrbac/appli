from rest_framework import serializers
from .models import WeatherCity

'''
Serializeri za modele gradova.
'''

# Serializer za elemente liste u podacima sa OWM API-ja.
# Jedan je lista sa ugniježđenim dictionary, pa zato je ovo za serijalizaciju ugniježđenih podataka.

class WeatherElemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    main = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=100)
    icon = serializers.CharField(max_length=100)
    class Meta:
        fields = '__all__'
        
# Serijalizacija podataka sa OWM API.
# Weather je lista, koja se onda slicea na templateu da prikazuje samo prvi dict.
        
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

# Generički Model Serializeri, fieldovi se mijenjaju ovisno o tome kojim se podacima daje pristup.

class CityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherCity
        fields = ('name', 'api_id',)
        
class CreateCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherCity
        fields = ('name', 'api_id',)

class UpdateCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherCity
        fields = ('name','favourite',)
        
class DeleteCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherCity
        fields = '__all__'    