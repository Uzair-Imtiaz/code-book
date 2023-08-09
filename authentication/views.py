"""
Views for user registration, login, and welcome in the 'authentication' app.

This file contains view classes and functions for handling user registration, login, and logout functionalities.
"""

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect, render, reverse
from django.views import View
from django.views.generic import DetailView, ListView

from core.models import Project

from authentication.forms import ProfileForm, SkillForm
from authentication.models import Profile
from authentication.utils import calculate_age


class RegisterView(View):
    """
    View class for user registration.

    This view handles both the GET and POST requests for user registration """

    def get(self, request):
        """ Handle the GET request for user registration. """

        if request.user.is_authenticated:
            messages.warning(request, 'Already signed in.')
            return redirect(reverse('authentication:profiles'))

        page = 'Register'
        return render(request, 'authentication/register.html', {'page': page})

    def post(self, request):
        """ Handle the POST request for user registration. """

        # import pdb; pdb.set_trace()
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')

            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, email=email, password=password)
                user.first_name = first_name
                user.last_name = last_name
                user.save()

            else:
                messages.warning(request, 'Username already exists. Sign in instead.')
                return render(request, 'authentication/sign_in.html')
            login(request, user)
            return redirect(reverse('authentication:edit-profile'))


class LoginView(View):
    """
    View class for user login.

    This view handles both the GET and POST requests for user login.
    """

    def get(self, request):
        """ Handle the GET request for user login. """

        if request.user.is_authenticated:
            messages.warning(request, 'Already signed in.')
            return redirect(reverse('authentication:profiles'))

        page = 'Login'
        return render(request, 'authentication/sign_in.html', {'page': page})

    def post(self, request):
        """ Handle the POST request for user login. """

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect(reverse('authentication:profiles'), {'user': user})

        else:
            messages.error(request, 'Wrong Credentials.')
            return render(request, 'authentication/sign_in.html')


class CreateOrEditProfileView(LoginRequiredMixin, View):
    """ View Class for creating a profile against a User instance """

    def get(self, request):
        """ Handles the GET request for profile creation. """

        page = 'Create Profile'
        user = request.user
        try:
            profile = user.profile
        except Profile.DoesNotExist:
            profile = None

        form = ProfileForm(instance=profile)
        context = {
            'page': page,
            'form': form,
            'profile': profile,
        }
        return render(request, 'authentication/edit-profile.html', context)

    def post(self, request):
        """
        Handles the POST request for profile creation.

        Receives the form submission and process the data to store it in the database as a profile instance.
        """

        user = request.user
        try:
            profile = user.profile
        except Profile.DoesNotExist:
            profile = None

        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            skills_ids = request.POST.getlist('skills')
            profile.skills.set(skills_ids)
            messages.success(request, 'Success!')
            return redirect(reverse('authentication:user-profile', kwargs={'pk': profile.id}))

        else:
            messages.error(request, 'An error occurred try again!')
            return render(request, 'authentication:edit-profile.html')


class CreateSkillView(LoginRequiredMixin, View):
    """ View class for creating a skill """

    def get(self, request):
        """ Handles the get request for the form """

        page = 'Add Skill'
        form = SkillForm()
        context = {
            'page': page,
            'form': form,
        }
        return render(request, 'authentication/skill-form.html', context)

    def post(self, request):
        """
        Handles the post request.

        Receives the data from the form and creates an instance of skill in the database.
        """

        form = SkillForm(request.POST)
        form.save()
        messages.success(request, 'Skill added successfully!')
        return redirect(reverse('authentication:profiles'))


class ProfilesView(ListView):
    """
    A view that displays all the profiles """

    page = 'Profiles'
    model = Profile
    template_name = 'authentication/profiles.html'
    context_object_name = 'profiles'


class UserProfileView(DetailView):
    """ A view that displays a specific profile"""

    model = Profile
    template_name = 'authentication/single-profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['page'] = profile.user.get_full_name()
        context['profile'] = profile
        context['projects'] = Project.objects.filter(user=profile.user)
        context['skills'] = profile.skills.all()
        context['age'] = calculate_age(profile.date_of_birth)
        return context


class LogoutView(LogoutView):
    """ View that handles the logout functionality """

    pass
