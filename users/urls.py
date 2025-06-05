from django.urls import path

from . import views
from .views import login_user, register_user

urlpatterns = [
    path('register',register_user,name='register'),
    path('login',login_user,name='login'),
]