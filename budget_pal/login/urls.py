from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',auth_views.LoginView.as_view(template_name='login/login_user.html'),name='login_user'),
    path('register/', views.register_user, name='register_user'), 
]