from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from .models import WeatherCity
from . import serializers, forms
from users import views as user_views
import requests
import pytemperature as pyt

def get_weather(city):
    apikey = '1eaaf038019381454dc2264f1dddf5b3'
    city = city.strip(' ')
    params = {'q':city, 'appid':apikey}
    url = f'https://api.openweathermap.org/data/2.5/weather/'
    weather_req = requests.get(url, params=params)
    return serializers.WeatherSerializer(weather_req.json()).data

# DRY funkcija za fiksnu listu sa strane
def sidelist(request):
    queryset = WeatherCity.objects.filter(featured=True)        
    serializer = serializers.CityListSerializer(queryset, many=True).data
    return serializer

# dodavanje grada u favorite
class FavouriteCity(APIView):
    def get(self, request, *args, **kwargs):
        if self.kwargs['name'] and self.kwargs['api_id']:
            #if not WeatherCity.objects.filter(name=self.kwargs['name']) and not WeatherCity.objects.filter(id=self.kwargs['api_id']):
            if not WeatherCity.objects.filter(api_id=self.kwargs['api_id']):
                city = WeatherCity(name=self.kwargs['name'].capitalize(), api_id=self.kwargs['api_id'])
                city.save()
            #     searched = self.kwargs['alter'].replace(" ","").lower()
            #     cityname = self.kwargs['name'].replace(" ","").lower()
            #     cities = WeatherCity.objects.all()
            #     city = ""
            #     for cty in cities:
            #         if cty.name.lower().replace(" ","") == searched:
            #             city = cty
            #         elif cty.name.lower().replace(" ","") == cityname:
            #             city = cty
            #     if not city:
            #         if searched == cityname:
            #             city = WeatherCity(name=self.kwargs['name'].capitalize(), api_id=self.kwargs['api_id'])
            #             city.save()
            #         else:
            #             city = WeatherCity(name=self.kwargs['alter'].capitalize())
            #             city.save()
            else:
                city = WeatherCity.objects.get(api_id=self.kwargs['api_id'])
            user = request.user
            city.favourite.add(user)
            city.save()
            return HttpResponseRedirect(reverse('city-weather', kwargs={'name': city.name}))
        
#micanje grada iz favorita
class UnfavouriteCity(APIView):
    def get(self, request, *args, **kwargs):
        if 'api_id' in self.kwargs:
            user = request.user
            city = WeatherCity.objects.filter(api_id=self.kwargs['api_id']).get()
            city.favourite.remove(user)
            city.save()
            return HttpResponseRedirect(reverse('city-weather', kwargs={'name': city.name}))       


### pogled na vrijeme u gradu

class CityWeatherView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    def get(self, request, *args, **kwargs):
        #lista unaprijed određenih gradova
        cities = sidelist(request)
        #pretraženi grad
        search_word = self.kwargs['name']        
        data = get_weather(self.kwargs['name'])
        data['main']['temp'] = pyt.k2f(data['main']['temp'])
        data['main']['feels_like'] = pyt.k2f(data['main']['feels_like'])
        # utvrđivanje je li grad favorit
        favourites = []
        fav = False
        if request.user.is_authenticated:
            favourites = user_views.favourites(request)
            for favor in favourites:
                if data['id'] == favor.api_id:
                    fav = True
        return Response({'data': data, 'city':search_word, 'favourites':favourites, 'fav':fav, 'cities':cities}, template_name='wetcity.html')
     
### homepage pogled
     
class BaseView(APIView):        
    renderer_classes = [TemplateHTMLRenderer]
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':            
            name = request.POST.get('name')
            return HttpResponseRedirect(reverse('city-weather', kwargs={'name':name}))
        
    def get(self, request, *args, **kwargs):
        favourites = []
        if request.user.is_authenticated:
            favourites = user_views.favourites(request)
        form = forms.SearchForm()
        cities = sidelist(request)
        return Response({'cities':cities, 'form':form, 'favourites': favourites}, template_name="base.html")
    
### strogi API
            
class CityListView(generics.ListAPIView):
    queryset = WeatherCity.objects.all()
    serializer_class = serializers.CityListSerializer

class CityCreateView(generics.CreateAPIView):
    queryset = WeatherCity.objects.all()
    serializer_class = serializers.CityCreateSerializer
    
class CityUpdateView(generics.UpdateAPIView):
    queryset = WeatherCity.objects.all()
    serializer_class = serializers.CityListSerializer
    
class WeatherView(APIView):    
    def get(self, request, *args, **kwargs):
        cities = WeatherCity.objects.all()
        cities = serializers.CityListSerializer(cities, many=True)
        data = get_weather(self.kwargs['name'])
        return Response({'data': data})
    