"""
URL configuration for the project.

This file defines the URL patterns for the project, mapping URLs to corresponding views.

URL patterns:
- '/auth/': Includes URL patterns from the 'authentication' app for user authentication and registration.
- '/admin/': Includes the Django admin site URL patterns.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('auth/', include('authentication.urls')),
    path('admin/', admin.site.urls),
]
