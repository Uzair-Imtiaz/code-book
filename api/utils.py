"""
This module contains utility functions related to skills and instances of Profile or Project models and to check
password strength.
"""

import re

from authentication.models import Skill


def add_skills_to_objects(instance, skill_names):
    """
    Add skills to the instance if they are not already associated.

    Try to get the skill instance from the Skills table, if not found it creates a skill of that name, add it to
    the object if not already associated.
    """

    if skill_names is not None:

        for skill_name in skill_names:
            skill, _ = Skill.objects.get_or_create(name__iexact=skill_name)

            if skill not in instance.skills.all():
                instance.skills.add(skill)


def is_strong_password(password):
    """ Checks if the password is strong """

    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$"
    return re.match(pattern, password)