from django.db import models
from contest.models import Mootcourt
from users.models import Profile
from django.utils.translation import gettext_lazy as _


class Document(models.Model):

    types = [('fabula', 'Fabula'), ('reglament', 'Reglament'), ('file', 'File'),
             ('procedural_document', 'Procedural document'), ('result_of_mootcourt', 'Result of moot court')]

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation date'))
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=_('Author'))
    document_type = models.CharField(max_length=25, choices=types, verbose_name=_('Document type'))
    file_name = models.CharField(max_length=255, verbose_name=_('File name'))
    icon = models.FileField(upload_to='icons/', verbose_name=_('Icon'))
    file = models.FileField(upload_to='documents/', verbose_name=_('File'))


class Message(models.Model):

    roles = [
        ('organization', 'University/organization'),
        ('participant', 'Participant'),
        ('coach', 'Coach'),
        ('referee', 'Referee')
    ]

    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation date'))
    date_published = models.DateTimeField(auto_now_add=True, verbose_name=_('Publication Date'))
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=_('Author'))
    text = models.TextField(verbose_name=_('Text'))
    recipient = models.CharField(max_length=15, choices=roles, default='participant', verbose_name=_('Recipient'))
    documents = models.ManyToManyField('Document', null=True, blank=True, verbose_name=_('Documents'))

    def __str__(self):
        return f"Message by {self.author} - {self.date_created}"


class Event(models.Model):

    types = [('registration', 'Registration of participants'), ('document_upload', 'Document upload'),
             ('online_conference', 'Online conference'), ('summarizing', 'Summarizing')]

    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation date'))
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=_('Author'))
    start_date = models.DateTimeField(verbose_name=_('Start'))
    end_date = models.DateTimeField(null=True, blank=True, verbose_name=_('End'))
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    description = models.TextField(verbose_name=_('Description'))
    event_type = models.CharField(max_length=50, choices=types, verbose_name=_('Event type'))
    file = models.ForeignKey('Document', null=True, blank=True,
                             on_delete=models.SET_NULL, verbose_name=_('Documents'))
    scheduled_video_conference_url = models.URLField(null=True, blank=True, verbose_name=_('Videoconference'))
    online_stream_url = models.URLField(null=True, blank=True, verbose_name=_('Stream'))

    def __str__(self):
        return self.title
