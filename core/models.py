""" This module contains models for the core app. """

from django.contrib.auth.models import User
from django.db import models
from model_utils.models import TimeStampedModel


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
    description = models.TextField(
        blank=True,
        null=True,
        help_text='The detailed description of the project.'
    )
    featured_image = models.ImageField(
        blank=True,
        null=True,
        help_text='The featured image(s) of the project.'
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
        help_text='The project that is being reviewed.'
    )
    body = models.TextField(
        blank=True,
        null=True,
        help_text='The content of the review.'
    )


class Vote(TimeStampedModel):
    """ A model representing a vote for a project """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='vote',
        help_text='The user who voted.'
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='project',
        help_text='The project being voted on.'
    )
    VoteChoices = models.TextChoices('Vote', 'Up, Down')
    vote = models.CharField(
        max_length=20,
        blank=True,
        choices=VoteChoices.choices,
        help_text='The vote choice (Up or Down).'
    )

    def __str__(self):
        return self.choices
