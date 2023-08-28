""" This module contains the serializers for all the models """

from django.contrib.auth.models import User
from django.utils.text import slugify
from rest_framework import serializers

from authentication.models import Profile, Skill
from core.models import Project, Review


class UserSerializerPost(serializers.ModelSerializer):
    """ User model serializer for post requests on users """

    class Meta:
        model = User
        fields = [
            'username', 'password', 'email', 'first_name', 'last_name'
        ]


class UserSerializer(serializers.ModelSerializer):
    """ Serializer for the User model for the response """

    profile_slug = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 'profile_slug', 'profile_picture',
        ]

    def get_profile_slug(self, obj):
        try:
            return obj.profile.slug
        except Profile.DoesNotExist:
            return None

    def get_profile_picture(self, obj):
        try:
            return obj.profile.profile_picture.url
        except Profile.DoesNotExist:
            return None


class SkillSerializer(serializers.ModelSerializer):
    """ Serializer for the Skill model """

    profile = serializers.SerializerMethodField()
    project = serializers.SerializerMethodField()

    class Meta:
        model = Skill
        fields = ['id', 'name', 'slug', 'description', 'profile', 'project']
        read_only_field = ['slug']

    def create(self, validated_data):
        """ Overridden to make sure the name is in title case and create a slug field """

        name = validated_data['name'] = validated_data['name'].title()
        if Skill.objects.filter(name=name).exists():
            raise serializers.ValidationError({"name": ["Skill with this name already exists."]})

        skill = Skill.objects.create(**validated_data)
        id_ = skill.id
        skill.slug = slugify('{}-{}'.format(id_, name))
        skill.save()
        return skill

    def get_profile(self, skill):
        """ Method to assign the related profiles to the SerializerMethodField """

        return skill.profile.all().values_list('user__username', flat=True)

    def get_project(self, skill):
        """ Method to assign the related projects to the SerializerMethodField """

        return skill.Project.all().values_list('title', flat=True)

    def to_representation(self, instance):
        """ Overridden to change how the profile and project instances are formatted in the response """

        representation = super().to_representation(instance)

        representation['profile'] = self.get_profile(instance)
        representation['project'] = self.get_project(instance)

        return representation


class ProjectSerializer(serializers.ModelSerializer):
    """ Serializer for the Project model """

    review = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        read_only_field = ['slug']
        model = Project
        fields = '__all__'

    def create(self, validated_data):
        """ Create method overridden to get the user that is sending the request to post the project """

        user = self.context['request'].user
        validated_data['user'] = user
        project = Project.objects.create(**validated_data)
        id_ = project.id
        title = project.title
        project.slug = slugify('{}-{}'.format(id_, title))
        project.save()
        return project

    def get_review(self, obj):
        """ Method that assigns the reviews to the Serializer field """

        review = Review.objects.filter(project=obj)
        return ReviewSerializer(review, many=True).data

    def to_representation(self, instance):
        """ Overridden to change the formatting of related fields in the response """

        representation = super().to_representation(instance)
        representation['skills'] = [skill['name'] for skill in representation['skills']]
        return representation


class ProfileSerializer(serializers.ModelSerializer):
    """ Serializer for the Profile model """

    user = UserSerializer(read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    project = ProjectSerializer(source='user.project', many=True, required=False)

    class Meta:
        model = Profile
        exclude = ['created', 'modified']
        read_only_field = ['slug']

    def create(self, validated_data):
        """ Create method overridden to get the user that is sending the request to post the project """

        user = self.context['request'].user
        validated_data['user'] = user
        id_ = user.id
        name = user.get_full_name()
        validated_data['slug'] = slugify(f'{id_}-{name}')

        profile = Profile.objects.create(**validated_data)
        return profile

    def to_representation(self, instance):
        """ Overridden to change the formatting of related fields in the response """

        representation = super().to_representation(instance)
        representation['skills'] = [skill['name'] for skill in representation['skills']]
        if 'project' in representation:
            representation['project'] = [project['title'] for project in representation['project']]
        return representation


class ReviewSerializer(serializers.ModelSerializer):
    """ Serializer for the Review model """

    user = UserSerializer(read_only=True)
    project = serializers.StringRelatedField()

    class Meta:
        model = Review
        exclude = ['modified']

