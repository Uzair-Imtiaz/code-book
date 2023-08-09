""" Registers the models of core app for interaction through admin interface."""

from django.contrib import admin

from core.models import Project, Review

admin.site.register(Project)
admin.site.register(Review)
