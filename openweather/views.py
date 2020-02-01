import requests
import pytemperature as pyt

from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from users import views as user_views
from .models import WeatherCity
from . import serializers, forms

# ger_weather: funkcija koja radi backend zahtjev prema OpenWeatherMap API endpointu.
# Prima string parametar te ga spušta na lowercase i uklanja razmake za smanjenje mogućnosti greške.
# APIkey za stranicu je ovdje u plain textu radi demonstracije, inače bi bio u env. varijablama.

def get_weather(city):
    apikey = '1eaaf038019381454dc2264f1dddf5b3'
    city = city.strip(' ')
    params = {'q':city, 'appid':apikey}
    url = f'https://api.openweathermap.org/data/2.5/weather/'
    weather_req = requests.get(url, params=params)
    weather_req = weather_req.json()    
    return serializers.WeatherSerializer(weather_req).data

# Funkcija koja dohvaća gradove na listi s lijeve strane kako je zadano u opisu zadatka.
# Odabrani gradovi nisu hardcoded u kodu, već su ručno dodani i označeni.
# Označeni su u bazi s featured (bool) atributom koji admini mogu mijenjati,
# te tako jednostavno određivati gradove koji će biti na listi.

def sidelist(request):
    queryset = WeatherCity.objects.filter(featured=True)        
    serializer = serializers.CityListSerializer(queryset, many=True).data
    return serializer

'''
Temeljni (home) pogled, kojeg ostali extendaju.
GET/POST requestovima razrađuje funkcionalnosti: POST šalje na detaljan prikaz odabranog grada.
Na njemu je search form, za temeljnu funkciju pretraživanja.  
Na svoj template proslijeđuje podatke: 
    - o gradovima koji su označeni da budu stalno na listi sa strane
    - o gradovima koji su u favoritima
    - o formi, tj samu formu.
    
    - ako se radi o POST metodi, proslijeđuje keyword argument na drugi prikaz.
'''
     
class BaseView(APIView):
    permission_classes = [permissions.AllowAny,]    
    renderer_classes = [TemplateHTMLRenderer]
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':        
            name = request.POST.get('name')
            return HttpResponseRedirect(reverse('city-weather', kwargs={'name':name}))
    
    def get(self, request, *args, **kwargs):
        favourite_cities = user_views.favourites(request)
        forma = forms.SearchForm()
        feat_cities = sidelist(request)
        return Response({'feat_cities': feat_cities, 'form': forma, 'favourite_cities': favourite_cities}, template_name="base.html")

### Ovaj pogled daje podatke o vremenu u pojedinom gradu. Koristi funkciju get_weather.
### Jedan od glavnih pogleda.
### Na njemu se nalazi opcija za označavanje favorita ili uklanjanje istih.

class CityWeatherView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
    
    def get(self, request, *args, **kwargs):
        # Lista unaprijed određenih gradova, kao i favorita
        feat_cities = sidelist(request)        
        favourite_cities = user_views.favourites(request)
        fav = False
        search_word = self.kwargs['name']
        try:
            data = get_weather(self.kwargs['name'])
        except:
            error = True
            return Response({'error':error, 'city':search_word, 'favourite_cities':favourite_cities, 'feat_cities':feat_cities}, template_name='wetcity.html')
        # Pretvorba temperature - pytemperature
        data['main']['temp'] = pyt.k2f(data['main']['temp'])
        data['main']['feels_like'] = pyt.k2f(data['main']['feels_like'])
        # utvrđivanje je li grad favorit
        if favourite_cities:            
            for favor in favourite_cities:
                if data['id'] == favor.api_id:
                    fav = True
        return Response({'data': data, 'city':search_word, 'favourite_cities':favourite_cities, 'fav':fav, 'feat_cities':feat_cities}, template_name='wetcity.html')

# Dodavanje grada u favorite. Ujedno i način dodavanja novih gradova u bazu, po potrebi tek ako netko doda u favorite.
# Prvo radi provjeru postoji li taj grad u bazi, ako ne dodaje ga.
# Nakon što je grad dodan, dodaje se u favorite.
# Za favorite se koristi ManyToManyField na strani grada.
# To je više na više relacija gdje Django sam stvara srednju tablicu.

class FavouriteCity(APIView):
    
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, f'Niste prijavljeni. Prijavite se kako biste mogli dodati favorite.')
            return HttpResponseRedirect(reverse('city-weather', kwargs={'name':self.kwargs['name']}))
        if self.kwargs['name'] and self.kwargs['api_id']:            
            if not WeatherCity.objects.filter(api_id=self.kwargs['api_id']):
                city = WeatherCity(name=self.kwargs['name'], api_id=self.kwargs['api_id'])
                if city.name == self.kwargs['name']:
                    city.save()
                elif city.name.lower == self.kwargs['name'].lower:
                    city.save()
                else: 
                    city.name = self.kwargs['name']
                    city.save()
            else:
                city = WeatherCity.objects.get(api_id=self.kwargs['api_id'])
            user = request.user
            city.favourite.add(user)
            city.save()
            return HttpResponseRedirect(reverse('city-weather', kwargs={'name': city.name}))
        
# Uklanjanje grada iz favorita.

class UnfavouriteCity(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    
    def get(self, request, *args, **kwargs):
        if 'api_id' in self.kwargs:
            user = request.user
            city = WeatherCity.objects.filter(api_id=self.kwargs['api_id']).get()
            city.favourite.remove(user)
            city.save()
            return HttpResponseRedirect(reverse('city-weather', kwargs={'name': city.name}))

### API sekcija: ne koristi se u templateima, no može se koristiti za CRUD funkcije. 
### Dozvole su određene za svaku zasebno, osvisno o potencijalnoj opasnosti.
            
class CityListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny,]
    queryset = WeatherCity.objects.all()
    serializer_class = serializers.CityListSerializer
    
class CreateCityView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = WeatherCity.objects.all()
    serializer_class = serializers.CityListSerializer
    
class UpdateCityView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = WeatherCity.objects.all()
    serializer_class = serializers.UpdateCitySerializer
    
class WeatherView(APIView):
    permission_classes = [permissions.AllowAny,]
    
    def get(self, request, *args, **kwargs):
        if self.kwargs['pk']:
            city = WeatherCity.objects.get(pk=self.kwargs['pk'])
            try:
                data = get_weather(city.name)
                return Response({'data': data})
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)

class DeleteCityView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAdminUser,]
    queryset = WeatherCity.objects.all()
    serializer_class = serializers.DeleteCitySerializer

class FavUnfavCity(APIView):
    serializer_class = serializers.UpdateCitySerializer
    permission_classes = [permissions.IsAuthenticated,]
    
    def get(self, request, *args, **kwargs):        
        if self.kwargs['name'] and self.kwargs['api_id']:            
            if not WeatherCity.objects.filter(api_id=self.kwargs['api_id']):
                city = WeatherCity(name=self.kwargs['name'].capitalize(), api_id=self.kwargs['api_id'])
                city.save()
            else:
                city = WeatherCity.objects.get(api_id=self.kwargs['api_id'])
            user = request.user
            city.favourite.add(user)
            city.save()
            return Response(status=status.HTTP_201_CREATED)
    
    def post(self, request, *args, **kwargs):
        if self.kwargs['api_id']:
            user = request.user
            city = WeatherCity.objects.filter(api_id=self.kwargs['api_id']).get()
            city.favourite.remove(user)
            city.save()
            return Response(status=status.HTTP_410_GONE)
