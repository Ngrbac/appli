from django.urls import path
from .views import (
    CityWeatherView,
    FavouriteCity,
    UnfavouriteCity,
    BaseView,
    )

urlpatterns = [
    path('', BaseView.as_view(), name='home'),
    path('weather/<str:name>/', CityWeatherView.as_view(), name='city-weather'),
    path('favourite/<str:name>/<int:api_id>/', FavouriteCity.as_view(), name='favourite'),
    path('unfavourite/<int:api_id>/', UnfavouriteCity.as_view(), name='unfavourite'),
]
