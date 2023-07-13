"""
Views for user registration, login, and welcome in the 'authentication' app.

This file contains view classes and functions for handling user registration, login, and logout functionalities.
"""

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, reverse
from django.views import View


class RegisterView(View):
    """
    View class for user registration.

    This view handles both the GET and POST requests for user registration.

    Methods:
    - get(request): Handles the GET request and renders the 'authentication/register.html' template with the 'page'
    context variable.
    - post(request): Handles the POST request and processes the form data for user registration.

    Attributes:
    - None
    """

    def get(self, request):
        """ Handle the GET request for user registration. """

        page = 'Register'
        return render(request, 'authentication/register.html', {'page': page})

    def post(self, request):
        """ Handle the POST request for user registration. """

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
                message = 'Username already exists. Sign in instead.'
                return render(request, 'authentication/sign_in.html', {'message': message})

            return redirect(reverse('authentication:create-profile'))


class LoginView(View):
    """
    View class for user login.

    This view handles both the GET and POST requests for user login.

    Methods:
    - get(request): Handles the GET request and renders the 'authentication/sign_in.html' template with the 'page'
    context variable.
    - post(request): Handles the POST request and authenticates the user based on the provided username and password.

    Attributes:
    - None
    """

    def get(self, request):
        """ Handle the GET request for user login. """

        page = 'Login'
        return render(request, 'authentication/sign_in.html', {'page': page})

    def post(self, request):
        """ Handle the POST request for user login. """

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect(reverse('authentication:welcome'), {'user': user})

            else:
                return render(request, 'authentication/sign_in.html', {'message': "Wrong Credentials!"})


def welcome(request):
    """
    Render the welcome page.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: Rendered 'authentication/welcome.html' template with the 'page' context variable.
    """

    page = 'Welcome'
    return render(request, 'authentication/welcome.html', {'page': page})
