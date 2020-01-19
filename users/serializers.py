from rest_framework import serializers
from django.contrib.auth.models import User
from openweather.serializers import CityListSerializer

# Serijalizacija podataka o korisnicima. Svaka akcija ima svoju radi različitih prava pristupa. 
# Npr. UserFullSerializer i UserSerializer: sva polja naspram "javnih"

class UserFullSerializer(serializers.ModelSerializer):
    weathercity_set = CityListSerializer(read_only=True, many=True)
    class Meta:
        model = User
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    weathercity_set = CityListSerializer(read_only=True, many=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'groups', 'date_joined', 'weathercity_set')
        
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        write_only_fields = ('password',)

    # Dorađena verzija serializera kako bi se hashirao password. 
    
    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        return validated_data
        
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        write_only_fields = ('password',)

class DeleteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
