import base64
from abc import ABC

from django.core.files.base import ContentFile
from drf_extra_fields.fields import Base64ImageField, Base64FileField
from filetype import filetype
from rest_framework import serializers

from contest.models import Mootcourt
from guides.models import Tag
from service.models import Event, Document, Message
from service.serializers import FileOrBase64Field
from .models import Profile, Team


class ProfileSerializer(serializers.ModelSerializer):
    photo = FileOrBase64Field(use_url=True, required=False)

    class Meta:
        model = Profile
        fields = ('first_name', 'position', 'photo', 'description', 'university_name', 'university_link',
                  'accept_team_invitations', 'phone', 'role', 'rating')


class RegistrationcompleteSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()


class TeamSerializer(serializers.ModelSerializer):
    coaches = serializers.PrimaryKeyRelatedField(
        queryset=Profile.objects.filter(role='coach'),
        many=True
    )
    members = serializers.PrimaryKeyRelatedField(
        queryset=Profile.objects.filter(role='participant'),
        many=True
    )

    class Meta:
        model = Team
        fields = "__all__"

    # def create(self, validated_data):
    #     coaches_data = validated_data.pop('coaches', [])
    #     members_data = validated_data.pop('members', [])
    #     team = Team.objects.create(**validated_data)
    #     team.coaches.set(coaches_data)
    #     team.members.set(members_data)
    #
    #     return team

    #
    # def update(self, instance, validated_data):
    #     # coaches_data = validated_data.pop('coaches', [])
    #     # members_data = validated_data.pop('members', [])
    #
    #     for key, value in validated_data.items():
    #         setattr(instance, key, value)
    #
