"""
URL configuration for the 'authentication' app.

This file defines the URL patterns for the 'authentication' app, mapping URLs to corresponding views.
"""

from django.urls import path

from . import views

app_name = 'authentication'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('welcome/', views.welcome, name='welcome'),
]
