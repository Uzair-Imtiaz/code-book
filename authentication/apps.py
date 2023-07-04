"""
Django application configuration for the 'authentication' app.

This file defines the configuration for the 'authentication' app, including the default auto-generated field type and
the app name.

Attributes:
- default_auto_field (str): The default auto-generated field type used by this app configuration.
- name (str): The name of the 'authentication' app.
"""

from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'
