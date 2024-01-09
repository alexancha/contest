from drf_extra_fields.fields import Base64FileField
from filetype import filetype
from rest_framework import serializers

from service.models import Document, Message, Event


# class Base64ImageField(serializers.ImageField):
#     """
#     Кастомное поле изображения для обработки закодированных в base64 изображений.
#     """
#
#     def to_internal_value(self, data):
#         if isinstance(data, str) and data.startswith('data:image'):
#             format, imgstr = data.split(';base64,')
#             ext = format.split('/')[-1]
#             data = ContentFile(base64.b64decode(imgstr), name=f'image.{ext}')
#             print(data)
#         return super().to_internal_value(data)


# class Base64FileField(serializers.FileField):
#     """
#     Кастомное поле изображения для обработки закодированных в base64 изображений.
#     """
#
#     def to_internal_value(self, data):
#         if isinstance(data, str) and data.startswith('data:'):
#             format, encoded_data = data.split(';base64,')
#             ext = format.split('/')[-1]
#             decoded_file = ContentFile(base64.b64decode(encoded_data), name=f'file.{ext}')
#             print(decoded_file)
#             return decoded_file
#
#         return super().to_internal_value(data)


class FileOrBase64Field(Base64FileField):

    ALLOWED_TYPES = ['pdf', 'jpg', 'jpeg', 'png', 'doc', 'xls', 'docx', 'xlsx']

    def get_file_extension(self, filename, decoded_file):
        return filetype.guess(decoded_file).extension


class DocumentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    icon = FileOrBase64Field(use_url=True, required=False)
    file = FileOrBase64Field(use_url=True, required=False)

    class Meta:
        model = Document
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    file = DocumentSerializer(many=True)

    class Meta:
        model = Event
        fields = '__all__'

    # def create(self, validated_data):
    #     print(validated_data)
    #     if 'file' in validated_data:
    #         documents_data = validated_data.pop('file')
    #         event = Event.objects.create(**validated_data)
    #         event.documents.set(documents_data)
    #         document = Document.objects.create(**documents_data)
    #         event.file.add(document)


class MessageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Message
        fields = '__all__'

    # def create(self, validated_data):
    #     print(validated_data)
    #     documents_data = validated_data.pop('documents', [])
    #     message = Message.objects.create(**validated_data)
    #     message.documents.set(documents_data)
#
#
# class TeamSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Team
#         fields = ('file_name', )
#
#
# class TagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tag
#         fields = ('name', )
