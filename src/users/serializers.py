import base64
from abc import ABC

from django.core.files.base import ContentFile
from rest_framework import serializers
from .models import Profile


class Base64ImageField(serializers.ImageField):
    """
    Кастомное поле изображения для обработки закодированных в base64 изображений.
    """

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'profile_image.{ext}')

        return super().to_internal_value(data)


class ProfileSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(use_url=True, required=False)

    class Meta:
        model = Profile
        fields = ('first_name', 'position', 'photo')


class RegistrationcompleteSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
