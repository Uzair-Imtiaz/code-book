"""
URL configuration for the project.

This file defines the URL patterns for the project, mapping URLs to corresponding views.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('authentication.urls')),
    path('core/', include('core.urls')),
    path('admin/', admin.site.urls),

    path('api/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
