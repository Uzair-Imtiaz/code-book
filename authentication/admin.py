""" Registers the models of authentication app for interaction through admin interface."""

from django.contrib import admin

from .models import *

admin.site.register(Profile)
admin.site.register(Skill)
