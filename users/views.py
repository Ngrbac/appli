from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView

from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.contrib.auth.models import User

from . import serializers, forms

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    
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

def favourites(request):
    user = request.user
    queryset = user.weathercity_set.all()
    return queryset