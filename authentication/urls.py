"""
URL configuration for the 'authentication' app.

This file defines the URL patterns for the 'authentication' app, mapping URLs to corresponding views.
"""

from django.urls import path

from authentication import views

app_name = 'authentication'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('edit-profile/', views.CreateOrEditProfileView.as_view(), name='edit-profile'),
    path('profile/<str:pk>', views.UserProfileView.as_view(), name='user-profile'),
    path('', views.ProfilesView.as_view(), name='profiles'),

    path('add-skill/', views.CreateSkillView.as_view(), name='add-skill'),
]
