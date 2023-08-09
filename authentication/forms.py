""" This module contains Django forms for handling Profile and Skill creation """

from django import forms
from sortedm2m.forms import SortedCheckboxSelectMultiple

from authentication.models import Profile, Skill


class ProfileForm(forms.ModelForm):
    """ A form for creating and updating user profiles """

    skills = SortedCheckboxSelectMultiple()

    class Meta:
        model = Profile
        exclude = ['user']

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        """ Giving class name form-control to all the form fields so that bootstrap can be applied """

        super(ProfileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class SkillForm(forms.ModelForm):
    """ A form for creating and updating skills """

    class Meta:
        model = Skill
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
