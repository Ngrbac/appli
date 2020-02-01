from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from users.views import register

# Glavno 'čvorište' URL-ova.
# Registracija, login i logout su na ovaj način izuzeti iz user dijela, gdje bi logički pripadali.

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', include('openweather.urls')),
    path('users/', include('users.urls')),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]
