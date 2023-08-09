"""
This file defines the configuration for the 'core' app, including the default auto-generated field type and
the app name.
"""
from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
