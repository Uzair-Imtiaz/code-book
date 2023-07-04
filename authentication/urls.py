"""
URL configuration for the 'authentication' app.

This file defines the URL patterns for the 'authentication' app, mapping URLs to corresponding views.

URL patterns:
- '/register/': Maps to the 'RegisterView' class-based view for user registration.
- '/login/': Maps to the 'LoginView' class-based view for user login.
- '/welcome/': Maps to the 'welcome' function-based view for the welcome page.
"""

from django.urls import path

from . import views

app_name = 'authentication'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('welcome/', views.welcome, name='welcome')
]
