"""
This file defines the configuration for the 'authentication' app, including the default auto-generated field type and
the app name.
"""

from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    """
    Configuration class for the 'authentication' app.

    Inherits from the base 'AppConfig' class and provides additional settings specific to the 'authentication' app.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'
