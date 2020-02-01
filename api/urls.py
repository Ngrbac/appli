from django.urls import path
from openweather.views import CreateCityView
from users.views import CreateUserView, UserFullListView, UserListView
from .views import UserManageView, CityManageView, FavouriteManageView

''' 
Struktura je posložena tako da okupi managere na istom endpointu,
uz managere idu i ostali API koji imaju različite endpointove.

Kreiranje gradova prima ime grada (kw='name') i njegov API id (kw='api_id') s OpenWeatherMap API-ja.
Kreiranje korisnika prima username, email i password (kw:'username', 'email', 'password').

Lista korisnika daje osnovne, nesenzitivne (relativno) podatke o korisnicima, dostupna svima.
Full lista korisnika daje sve podatke o korisnicima, dostupna samo admin/superuser korisnicima.

'''

urlpatterns = [
    path('users/<int:pk>/', UserManageView.as_view()),
    path('cities/<int:pk>/', CityManageView.as_view()),
    path('fav/<int:api_id>/<str:name>/', FavouriteManageView.as_view()),
    path('cities/create/', CreateCityView.as_view()),
    path('users/create/', CreateUserView.as_view()),
    path('users/list/', UserListView.as_view()),
    path('users/full/', UserFullListView.as_view()),
]