""" This module contains models for the core app. """

from django.contrib.auth.models import User
from django.db import models
from model_utils.models import TimeStampedModel
from sortedm2m.fields import SortedManyToManyField

from authentication.models import Skill


class Project(TimeStampedModel):
    """ A model representing a project """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        related_name='project',
        help_text='The user that created the project.'
    )
    title = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text='The title of the project.'
    )
    slug = models.SlugField(
        blank=True,
        null=True,
        max_length=50,
        unique=True,
        help_text='Combination of id and title as a lookup field.'
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text='The detailed description of the project.'
    )
    featured_image = models.ImageField(
        upload_to='projects/',
        default='projects/default.jpg',
        blank=True,
        null=True,
        help_text='The featured image of the project.'
    )
    youtube_link = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text='The link to the YouTube video of the project.'
    )
    demo_link = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text='The link to the demo of the project(if deployed).'
    )
    source_code_link = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text='The link to the source code of the project.'
    )
    skills = SortedManyToManyField(
        Skill,
        blank=True,
        related_name='Project',
        help_text='The relevant skills in the project.'
    )

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.title


class Review(TimeStampedModel):
    """ A model representing a review for a project """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='review',
        help_text='The user who wrote the review.'
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='review',
        help_text='The project that is being reviewed.'
    )
    VoteChoices = models.TextChoices('Vote', 'Up, Down')
    vote = models.CharField(
        max_length=20,
        blank=True,
        choices=VoteChoices.choices,
        help_text='The vote choice (Up or Down).'
    )
    body = models.TextField(
        blank=True,
        null=True,
        help_text='The content of the review.'
    )

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.vote
