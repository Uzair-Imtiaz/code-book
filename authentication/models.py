""" This module contains models for the authentication app. """

from django.contrib.auth.models import User
from django.db import models
from model_utils.models import TimeStampedModel
from sortedm2m.fields import SortedManyToManyField


class Profile(TimeStampedModel):
    """ Model representing a user profile """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text='The related user.'
    )
    skills = SortedManyToManyField(
        'Skill',
        blank=True,
        related_name='profile',
        help_text='The skills associated with the profile.'
    )
    short_intro = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='A short intro or a post title.'
    )
    bio = models.TextField(
        blank=True,
        null=True,
        help_text='A detailed bio of the user about themselves.'
    )
    profile_picture = models.ImageField(
        upload_to='profiles/',
        default='profiles/user-default.png',
        blank=True,
        null=True,
        help_text='A profile picture of the user.'
    )
    github = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text='The GitHub profile link.'
    )
    linkedin = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text='The LinkedIn profile link.'
    )
    youtube = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text='The YouTube profile link.'
    )

    GenderChoices = models.TextChoices('Gender', 'Male, Female')
    gender = models.CharField(
        max_length=20,
        blank=True,
        choices=GenderChoices.choices,
        help_text='The gender of the user.'
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True,
        help_text='The date of birth of the user.'
    )

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        ordering = ['created']


class Skill(TimeStampedModel):
    """ Model representing a skill """

    name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text='The name of the skill.'
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text='A description of the skill.'
    )

    def __str__(self):
        return self.name
