from django.forms.widgets import SelectMultiple


class MultipleChoiceAddWidget(SelectMultiple):
    template_name = 'authentication/edit-profile.html'
    can_add_skills = False

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['can_add_skills'] = self.can_add_skills
        return context
