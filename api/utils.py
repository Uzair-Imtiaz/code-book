"""
This module contains utility functions related to skills and instances of Profile or Project models and to check
password strength.
"""

import re

from api.serializers import SkillSerializer
from authentication.models import Skill


def add_skills_to_objects(instance, skill_names):
    """
    Add skills to the instance if they are not already associated.

    Try to get the skill instance from the Skills table, if not found it creates a skill of that name, add it to
    the object if not already associated.
    """

    if skill_names is not None:

        for skill_name in skill_names:
            try:
                skill = Skill.objects.get(name__iexact=skill_name)
            except Skill.DoesNotExist:
                serializer = SkillSerializer(data={'name': skill_name})
                if serializer.is_valid():
                    skill = serializer.save()
                else:
                    return

            if skill not in instance.skills.all():
                instance.skills.add(skill)


def is_strong_password(password):
    """ Checks if the password is strong """

    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$"
    return re.match(pattern, password)
