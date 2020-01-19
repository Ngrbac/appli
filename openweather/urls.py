from django.urls import path
from .views import CityListView, CityWeatherView, CityCreateView, CityUpdateView, BaseView, FavouriteCity, WeatherView, UnfavouriteCity

urlpatterns = [
    path('', BaseView.as_view(), name='home'),
    path('cities/', CityListView.as_view(), name='city-list'),
    path('create-city/', CityCreateView.as_view(), name='city-create'),
    path('update-city/<int:pk>/', CityUpdateView.as_view(), name='city-update'),
    path('weather/<str:name>/', CityWeatherView.as_view(), name='city-weather'),
    path('apiweather/<str:name>/', WeatherView.as_view(), name='city-weather-api'),
    path('favourite/<str:name>/<int:api_id>/', FavouriteCity.as_view(), name='favourite'),
    path('unfavourite/<int:api_id>/', UnfavouriteCity.as_view(), name='unfavourite'),
]
