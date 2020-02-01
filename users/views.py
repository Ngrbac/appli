from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from openweather.views import sidelist
from . import serializers, forms

# Funkcija izvršava registraciju.
# Forma je default django: UserRegisterForm koja sama po sebi vrši hash lozinke.
# Na GET metodu daje formu za registraciju, na POST validira podatke i pohranjuje novog korisnika.

def register(request):
    if request.method == 'POST':
        form = forms.UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created, {username}! You are now able to log in')
            return redirect('login')
    else:
        form = forms.UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

# Funkcija za pronalaženje omiljenih gradova. 
# Vraća queryset gradova koje je trenutni korisnik obilježio kao omiljene.

def favourites(request):
    queryset = 0
    if request.user.is_authenticated:
        user = request.user
        queryset = user.weathercity_set.all()
        return queryset
    else:
        return queryset

class Profile(generics.RetrieveAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    
    def get(self, request, *args, **kwargs): 
        feat_cities = sidelist(request)        
        favourite_cities = favourites(request)       
        if request.user.pk == self.kwargs['pk']:
            user = request.user
            user = serializers.UserSerializer(user).data
            return Response({'current_user':user, 'feat_cities':feat_cities, 'favourite_cities':favourite_cities }, template_name='profile.html')
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

### API sekcija: ne koristi se u templateima, no može se koristiti za CRUD funkcije.
### Dozvole su određene za svaku zasebno, osvisno o potencijalnoj opasnosti.

class UserFullListView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    serializer_class = serializers.UserFullSerializer

class UserListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    
class DetailUserView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    
class CreateUserView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()    
    serializer_class = serializers.CreateUserSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = serializers.CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class DeleteUserView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    serializer_class = serializers.DeleteUserSerializer
    
class UpdateUserView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()    
    serializer_class = serializers.UpdateUserSerializer
    