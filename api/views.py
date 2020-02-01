from rest_framework.response import Response
from rest_framework.views import APIView
from users.views import (    
    DeleteUserView,
    UpdateUserView,
    DetailUserView,    
    )
from openweather.views import (
    UpdateCityView, 
    DeleteCityView,
    WeatherView,  
    FavUnfavCity,  
)

# API aplikacija u projektu služi za grupiranje URI-ja kako bi se odvojili data API-ji od ostalih koji su korišteni za templateove.
# Postavljanje osnovnog managera/dispatchera za requestove koji imaju istu strukturu ali različite metode.

class BaseManageView(APIView):
    
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, 'VIEWS_BY_METHOD'):
            raise Exception('VIEWS_BY_METHOD static dictionary variable must be defined on a ManageView class!')
        if request.method in self.VIEWS_BY_METHOD:
            return self.VIEWS_BY_METHOD[request.method]()(request, *args, **kwargs)

        return Response(status=405)

# Manager za pregled, brisanje i izmjenu korisnika, manager bira koji će se izvršiti na temelju metode.

class UserManageView(BaseManageView):
    VIEWS_BY_METHOD = {
        'GET': DetailUserView.as_view,
        'DELETE': DeleteUserView.as_view,        
        'PATCH': UpdateUserView.as_view,
    }

# Kao prethodni, samo za gradove.

class CityManageView(BaseManageView):
    VIEWS_BY_METHOD = {        
        'GET': WeatherView.as_view,
        'DELETE': DeleteCityView.as_view,        
        'PATCH': UpdateCityView.as_view,
    }

# Manager za favorite. GET dodaje favorita za trenutnog korisnika, POST ga uklanja.

class FavouriteManageView(BaseManageView):
    VIEWS_BY_METHOD = {
        'GET': FavUnfavCity.as_view,
        'POST': FavUnfavCity.as_view,
    }
