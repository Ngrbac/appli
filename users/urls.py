from django.urls import path, include
from .views import UserListView, register
urlpatterns = [    
    path('register/', register, name='register'),
    path('', UserListView.as_view(), name='users'),
]
