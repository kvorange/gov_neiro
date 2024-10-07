from django.urls import path
from .api.auth import registration, login

urlpatterns = [
    path('users/registration', registration),
    path('users/login', login),
]
