""" A form for creating and updating project instances """

from django import forms
from django.forms import ModelForm
from sortedm2m.forms import SortedCheckboxSelectMultiple

from core.models import Project, Review


class ProjectForm(ModelForm):
    """ A form for creating and updating project instances """

    skills = SortedCheckboxSelectMultiple()

    class Meta:
        model = Project
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ReviewForm(ModelForm):
    """ A form for creating and updating review instances for projects """

    class Meta:
        model = Review
        fields = ['body', 'vote']

        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-input'}),
        }
