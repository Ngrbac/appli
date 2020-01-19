from django.urls import path
from .views import (
    register,
    Profile,
    UserListView,
    CreateUserView,
    DeleteUserView,
    UpdateUserView,
)

urlpatterns = [    
    path('', UserListView.as_view(), name='users'),
    path('profile/<int:pk>/', Profile.as_view(), name='profile'),
    path('create/', CreateUserView.as_view(), name='create-user'),
    path('delete/<int:pk>/', DeleteUserView.as_view(), name='delete-user'),
    path('update/<int:pk>/', UpdateUserView.as_view(), name='update-user'),
]
