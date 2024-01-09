from django.core.exceptions import ObjectDoesNotExist

from contest.models import Mootcourt
from service.models import Document, Event, Message
from service.serializers import EventSerializer, MessageSerializer, DocumentSerializer
from users.models import Profile

from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers


class MootcourtSerializer(serializers.ModelSerializer):
    image = Base64ImageField(use_url=True, required=False)
    referees = serializers.PrimaryKeyRelatedField(
        queryset=Profile.objects.filter(role='referee'),
        many=True
    )
    senior_referees = serializers.PrimaryKeyRelatedField(
        queryset=Profile.objects.filter(role='referee'),
        many=True
    )
    events = EventSerializer(many=True)
    documents = DocumentSerializer(many=True)
    messages = MessageSerializer(many=True)

    class Meta:
        model = Mootcourt
        fields = "__all__"

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #
    #     # Преобразуйте идентификаторы в имена тегов, рефери и т.д.
    #     representation['tags'] = [tag.name for tag in instance.tags.all()]
    #     representation['senior_referees'] = [referee.first_name for referee in instance.senior_referees.all()]
    #     representation['referees'] = [referee.first_name for referee in instance.referees.all()]
    #     # representation['documents'] = [document.file_name for document in instance.documents.all()]
    #     # representation['events'] = [event.title for event in instance.events.all()]
    #     representation['teams'] = [team.name for team in instance.teams.all()]
    #     # representation['messages'] = [message.name for message in instance.messages.all()]
    #     return representation

    def create(self, validated_data):
        events_data = validated_data.pop('events', [])
        referees_data = validated_data.pop('referees', [])  # Получаем список судей из валидированных данных
        senior_referees_data = validated_data.pop('senior_referees', [])
        tags_data = validated_data.pop('tags', [])
        messages_data = validated_data.pop('messages', [])
        documents_data = validated_data.pop('documents', [])
        teams_data = validated_data.pop('teams', [])

        mootcourt = Mootcourt.objects.create(**validated_data)
        mootcourt.referees.set(referees_data)
        mootcourt.senior_referees.set(senior_referees_data)
        mootcourt.tags.set(tags_data)
        mootcourt.teams.set(teams_data)

        for event_data in events_data:
            if 'file' in event_data:
                documents_event_data = event_data.pop('file')
                event_instance = Event.objects.create(**event_data)
                mootcourt.events.add(event_instance)
                for document_event_data in documents_event_data:
                    document = Document.objects.create(**document_event_data)
                    event_instance.file.add(document)
            else:
                event_instance = Event.objects.create(**event_data)
                mootcourt.events.add(event_instance)

        for document_data in documents_data:
            document_instance = Document.objects.create(**document_data)
            mootcourt.documents.add(document_instance)

        for message_data in messages_data:
            documents_message_data = message_data.pop('documents', [])
            message_instance = Message.objects.create(**message_data)
            message_instance.documents.set(documents_message_data)
            mootcourt.messages.add(message_instance)

        return mootcourt

    def update(self, instance, validated_data):
        print(validated_data)
        events_data = validated_data.pop('events', [])
        print(events_data)
        messages_data = validated_data.pop('messages', [])
        documents_data = validated_data.pop('documents', [])
        # instance.title = validated_data.get('title', instance.title)
        # instance.event_type = validated_data.get('event_type', instance.event_type)
        # instance.announcement = validated_data.get('announcement', instance.announcement)
        # instance.status_moot_court = validated_data.get('status_moot_court', instance.status_moot_court)
        # instance.status = validated_data.get('status', instance.status)
        # instance.organizer = validated_data.get('organizer', instance.organizer)
        # instance.need_telegram_channel = validated_data.get('need_telegram_channel', instance.need_telegram_channel)
        # instance.telegram_channel = validated_data.get('telegram_channel', instance.telegram_channel)
        # instance.background = validated_data.get('background', instance.background)
        # instance.image = validated_data.get('image', instance.image)
        # instance.display_on_main = validated_data.get('display_on_main', instance.display_on_main)
        # instance.referees.set(validated_data.get('referees', instance.referees))
        # instance.senior_referees.set(validated_data.get('senior_referees', instance.senior_referees))
        # instance.teams.set(validated_data.get('teams', instance.teams))
        # instance.tags.set(validated_data.get('tags', instance.tags))

        super().update(instance, validated_data)
        if events_data:
            # events_data = validated_data.get('events', [])
            print(events_data)
            current_events = instance.events.all()
            events_to_remove = current_events.exclude(id__in=[event_data.get('id') for event_data
                                                              in events_data if event_data.get('id')])

            for event_to_remove in events_to_remove:
                instance.events.remove(event_to_remove)
            # instance.events.clear()
            for event_data in events_data:
                if 'file' in event_data:
                    documents_event_data = event_data.pop('file')
                    event_id = event_data.get('id')
                    if event_id:
                        try:
                            event_instance = Event.objects.get(id=event_id)
                            if event_instance not in current_events:
                                instance.events.add(event_instance)
                            for key, value in event_data.items():
                                setattr(event_instance, key, value)
                            event_instance.save()

                        except ObjectDoesNotExist:
                            event_instance = Event.objects.create(**event_data)
                            instance.events.add(event_instance)

                    else:
                        event_instance = Event.objects.create(**event_data)
                        instance.events.add(event_instance)

                    current_documents = event_instance.file.all()
                    documents_to_remove = current_documents.exclude(id__in=[document_data.get('id') for document_data
                                                                            in documents_event_data
                                                                            if document_data.get('id')])

                    for document_to_remove in documents_to_remove:
                        event_instance.file.remove(document_to_remove)

                    for document_event_data in documents_event_data:
                        document_id = document_event_data.get('id')
                        if document_id:
                            try:
                                document_instance = Document.objects.get(id=document_id)
                                if document_instance not in current_documents:
                                    instance.documents.add(document_instance)
                                for key, value in document_event_data.items():
                                    setattr(document_instance, key, value)
                                document_instance.save()

                            except ObjectDoesNotExist:
                                document_instance = Document.objects.create(**document_event_data)
                                instance.documents.add(document_instance)
                        else:
                            document_instance = Document.objects.create(**document_event_data)
                            instance.documents.add(document_instance)
                        event_instance.file.add(document_instance)
                else:
                    event_id = event_data.get('id')
                    if event_id:
                        try:
                            event_instance = Event.objects.get(id=event_id)
                            if event_instance not in current_events:
                                instance.events.add(event_instance)
                            for key, value in event_data.items():
                                setattr(event_instance, key, value)
                            event_instance.save()

                        except ObjectDoesNotExist:
                            event_instance = Event.objects.create(**event_data)
                            instance.events.add(event_instance)

                    else:
                        event_instance = Event.objects.create(**event_data)
                        instance.events.add(event_instance)

        if documents_data:
            current_documents = instance.documents.all()
            documents_to_remove = current_documents.exclude(id__in=[document_data.get('id') for document_data
                                                                    in documents_data if document_data.get('id')])

            for document_to_remove in documents_to_remove:
                instance.documents.remove(document_to_remove)

            for document_data in documents_data:
                document_id = document_data.get('id')
                if document_id:
                    try:
                        document_instance = Document.objects.get(id=document_id)
                        if document_instance not in current_documents:
                            instance.documents.add(document_instance)
                        for key, value in document_data.items():
                            setattr(document_instance, key, value)
                        document_instance.save()

                    except ObjectDoesNotExist:
                        document_instance = Document.objects.create(**document_data)
                        instance.documents.add(document_instance)
                else:
                    document_instance = Document.objects.create(**document_data)
                    instance.documents.add(document_instance)

        if messages_data:
            current_messages = instance.messages.all()
            messages_to_remove = current_messages.exclude(id__in=[message_data.get('id') for message_data
                                                                  in messages_data if message_data.get('id')])

            for message_to_remove in messages_to_remove:
                instance.messages.remove(message_to_remove)

            for message_data in messages_data:
                documents_message_data = message_data.pop('documents', [])
                message_id = message_data.get('id')
                if message_id:
                    try:
                        message_instance = Message.objects.get(id=message_id)
                        if message_instance not in current_messages:
                            instance.messages.add(message_instance)
                        for key, value in message_data.items():
                            setattr(message_instance, key, value)
                        message_instance.documents.set(documents_message_data)
                        message_instance.save()

                    except ObjectDoesNotExist:
                        message_instance = Document.objects.create(**message_data)
                        message_instance.documents.set(documents_message_data)
                        instance.messages.add(message_instance)
                else:
                    message_instance = Message.objects.create(**message_data)
                    message_instance.documents.set(documents_message_data)
                    instance.messages.add(message_instance)

        instance.save()
        return instance
