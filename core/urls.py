""" URL configuration for the 'core' app."""

from django.urls import path

from core import views

app_name = 'core'

urlpatterns = [
    path('add-project/', views.AddOrEditProjectView.as_view(), name='add-project'),
    path('edit-project/<str:pk>/', views.AddOrEditProjectView.as_view(), name='edit-project'),
    path('projects/', views.ProjectsView.as_view(), name='projects'),
    path('project<str:pk>', views.SingleProjectView.as_view(), name='project'),
    path('project/<str:pk>/delete', views.DeleteProjectView.as_view(), name='delete-project'),

    path('add-review/<str:pk>', views.AddReview.as_view(), name='add-review')
]
