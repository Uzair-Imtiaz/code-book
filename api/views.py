""" This module contains the ViewSets """

from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from rest_framework import generics, permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response

from api.permissions import IsOwnerOrReadOnly
from api.serializers import *
from api.utils import add_skills_to_objects, is_strong_password


class AuthViewSet(viewsets.GenericViewSet):
    """ API endpoint for user authentication and registration """

    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @action(methods=['post'], detail=False)
    def login(self, request):
        """
        Action to handle user login.

        Example Request (POST):
            {
                "username": "john_doe",
                "password": "password"
            }

            Example Response (HTTP 200 OK):
            {
                "token": "key"
            }

            Example Response (HTTP 401 Unauthorized):
            {
                "error": "Invalid credentials."
            }
            """

        username = request.data.get('username').lower()
        password = request.data.get('password')

        if len(username) == 0 or len(password) == 0:
            return Response({'error': 'Please provide both username and password.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            user = UserSerializer(user)
            return Response({'token': token.key, 'user': user.data}, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        """"""

        logout(request)
        return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def register(self, request):
        """
        Action to handle registration of a user.

        Example request (POST)
        {
            "username": "new_user",
            "password": "new_secure_password",
            "email": "new_user@example.com",
            "first_name": "John",
            "last_name": "Doe"
        }

        Example Response (HTTP 201 Created):
        {
            "message": "Registration successful.",
            "user": {
                "id": 123,
                "username": "new_user",
                "email": "new_user@example.com",
                "first_name": "John",
                "last_name": "Doe"
            }
        }

        Example Response (HTTP 409 Conflict):
        {
            "message": "Username already exists. Please choose a different username."
        }
        """

        serializer = UserSerializerPost(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username'].lower()
            password = serializer.validated_data['password']
            serializer.validated_data['username'] = username
            serializer.validated_data['first_name'] = serializer.validated_data['first_name'].title()
            serializer.validated_data['last_name'] = serializer.validated_data['last_name'].title()

            if not is_strong_password(password):
                return Response({'error': 'Weak password'}, status=status.HTTP_406_NOT_ACCEPTABLE)

            if User.objects.filter(username=username).exists():
                return Response({'error': 'Username already exists. Please choose a different username.'},
                                status=status.HTTP_409_CONFLICT)

            user = User.objects.create_user(**serializer.validated_data)
            user.set_password(password)
            return Response({'user': UserSerializerPost(user).data},
                            status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows viewing or editing user profiles """

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    def create(self, request, *args, **kwargs):
        """
        API endpoint for creating a new profile with optional skills association.

        A list of skill names to associate with the created object. If provided, the method will create the profile
        and associate it with the specified skills.

        Example Request (POST):
        {
            "short_intro": "intro",
            "bio": "BIO",
            "skills": ["Skill A", "Skill B"]
        }

        Example Response (HTTP 201 Created):
        {
            "id": 123,
            "user": user.username,
            "short_intro": "intro",
            "skills": [1, 2]
        }

        Example Response (HTTP 400 Bad Request):
        {
            "name": ["This field is required."]
        }
        """

        skill_names = request.data.get('skills').split(' ')
        serializer = self.get_serializer(data=request.data)
        user = request.user

        if serializer.is_valid():

            if Profile.objects.filter(user=user).exists():
                return Response({'error': 'Profile with this user already exists.'}, status=status.HTTP_409_CONFLICT)

            profile = serializer.save()
            add_skills_to_objects(profile, skill_names)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        """
        API endpoint for partially updating a user profile.

        A list of skill names to add to the user's profile. If provided, the method will associate the user
        with the specified skills.

        Example Request (PATCH):
        {
            "skills": ["Python", "JavaScript", "React"]
        }

        Example Response (HTTP 200 OK):
        {
            "id": 123,
            "user": 456,
            "skills": [1, 2, 3]
            // Other profile fields
        }

        Example Response (HTTP 404 NOT FOUND):
        {
            "error": "Profile does not exist."
        }
        """

        skill_names = request.data.get('skills').split(' ')
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response({'error': 'Profile does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        current_skills = list(profile.skills.all())
        add_skills_to_objects(profile, skill_names)

        for skill in current_skills:
            if skill.name not in skill_names:
                profile.skills.remove(skill)

        response = super().partial_update(request, *args, **kwargs)
        return response

    def perform_create(self, serializer):
        """ Assign user from the request to the profile instance """

        user = self.request.user
        serializer.save(user=user)

    def get_queryset(self):
        """ Get the queryset of profiles filtered by the provided keyword """

        search = self.request.query_params.get('search', '')
        queryset = Profile.objects.filter(
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(skills__name__icontains=search)
        ).distinct()
        return queryset

    @action(methods=['get'], detail=True, url_name='profile_projects', url_path='projects',
            permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def profile_projects(self, request, slug):
        """ Action endpoint to get the list of all the projects of a profile """

        try:
            profile = Profile.objects.get(slug=slug)
        except Profile.DoesNotExist:
            return Response({'error': 'Profile does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        projects = Project.objects.filter(user_id=profile.user_id)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True, url_name='profile_skills', url_path='skills')
    def profile_skills(self, request, slug):
        """ Action endpoint to get the list of all the skills for a profile """

        try:
            profile = Profile.objects.get(slug=slug)
        except Profile.DoesNotExist:
            return Response({'error': 'Profile does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        skills = profile.skills.all()
        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data)


class ProjectViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows viewing or editing user projects """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    def create(self, request, *args, **kwargs):
        """
        API endpoint for creating a new project with optional skills association.

        skill_names (list):
        A list of skill names to associate with the created object. If provided, the method will create the project
        and associate it with the specified skills.

        Example Request (POST):
        {
           "title": "Project",
           "description": "DESC",
           "skills": ["Skill A", "Skill B"]
        }

        Example Response (HTTP 201 Created):
        {
           "id": 123,
           "name": "Project",
           "description": "DESC",
           "skills": [1, 2]
           // Other object fields
        }

        Example Response (HTTP 400 Bad Request):
        {
           "name": ["This field is required."]
        }
        """

        skill_names = request.data.get('skills').split(' ')
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            project = serializer.save()
            add_skills_to_objects(project, skill_names)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        """
        API endpoint for partially updating a project with optional skills association.

        skill_names (list):
        A list of skill names to associate with the updated project. If provided, the method will update the project
        and associate it with the specified skills.

        Example Request (PATCH):
        URL: /projects/{project_id}/
        {
            "title": "Updated Project",
            "description": "An updated project description",
            "skills": ["Skill A", "Skill B"]
        }

        Example Response (HTTP 200 OK):
        {
            "id": 123,
            "title": "Updated Project",
            "description": "An updated project description",
            "skills": [1, 2]
            // Other project fields
        }

        Example Response (HTTP 404 NOT FOUND):
        {
            "error": "Project does not exist."
        }
        """

        skill_names = request.data.get('skills').split(' ')

        try:
            project = self.get_object()
        except Project.DoesNotExist:
            return Response({'error': 'Project does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        current_skills = list(project.skills.all())
        add_skills_to_objects(project, skill_names)

        for skill in current_skills:
            if skill.name not in skill_names:
                project.skills.remove(skill)

        response = super().partial_update(request, *args, **kwargs)
        return response

    def destroy(self, request, *args, **kwargs):
        """ API endpoint to delete a project instance by an authorised user """

        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'Deleted': 'Object deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        """ Get the queryset of projects filtered by the provided keyword """

        search = self.request.query_params.get('search', '')

        queryset = Project.objects.filter(
            Q(title__icontains=search) |
            Q(skills__name__icontains=search) |
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search)
        ).distinct()
        return queryset

    @action(methods=['get'], detail=True, url_path='skills', url_name='project_skills')
    def project_skills(self, request, slug):
        """ Action endpoint to get the list of all the skills associated with the project """

        try:
            project = Project.objects.get(slug=slug)
        except Project.DoesNotExist:
            return Response({'error': 'Project does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        skills = project.skills.all()
        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data)

    @action(methods=['get', 'post', 'delete'], detail=True, url_path='reviews',
            permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def project_reviews(self, request, slug):
        """
        API endpoint to handle the viewing, adding and deleting of the reviews on the project by the authorised user.
        """

        try:
            project = Project.objects.get(slug=slug)
        except Project.DoesNotExist:
            return Response({'error': 'Project does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'POST':
            serializer = ReviewSerializer(data=request.data)

            if serializer.is_valid():

                if request.user == project.user:
                    return Response({'error': 'You can\'t comment on your own project.'},
                                    status=status.HTTP_405_METHOD_NOT_ALLOWED)

                elif project.review.filter(user=request.user).exists():
                    return Response({'error': 'You have already submitted your review for this project.'},
                                    status=status.HTTP_403_FORBIDDEN)

                validated_data = serializer.validated_data
                review = Review.objects.create(**validated_data, user=request.user, project=project)
                return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)


            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            try:
                review = project.review.get(user=request.user)
            except Review.DoesNotExist:
                return Response({'error': 'Review does not exist.'}, status=status.HTTP_404_NOT_FOUND)

            review.delete()
            return Response({'success': 'Review deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

        else:
            reviews = project.review.all()
            serializer = ReviewSerializer(reviews, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReviewAPIView(generics.ListAPIView):
    """ API endpoint to list all the reviews """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class SkillViewSet(viewsets.ModelViewSet):
    """ API endpoint to handle viewing and editing ond the skills """

    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    lookup_field = 'slug'
