from django.db import models
from django.utils import timezone
from filetype import filetype

from users.models import Profile
from django.utils.translation import gettext_lazy as _


class Document(models.Model):

    types = [('fabula', 'Fabula'), ('reglament', 'Reglament'), ('file', 'File'),
             ('procedural_document', 'Procedural document'), ('result_of_mootcourt', 'Result of moot court')]

    created_at = models.DateTimeField(default=timezone.now, verbose_name=_('Creation Date'))
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=_('Author'))
    document_type = models.CharField(max_length=25, choices=types, verbose_name=_('Document type'))
    file_name = models.CharField(max_length=255, verbose_name=_('File name'))
    icon = models.FileField(upload_to='icons/', verbose_name=_('Icon'), blank=True)
    file = models.FileField(upload_to='documents/', verbose_name=_('File'), blank=True)

    def save(self, *args, **kwargs):
        if filetype.guess(self.file).extension in ["doc", "docx"]:
            self.icon = "icons/word.png"
        if filetype.guess(self.file).extension in ["xls", "xlsx"]:
            self.icon = "icons/excel.png"
        if filetype.guess(self.file).extension == "pdf":
            self.icon = "icons/pdf.png"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.file_name

class Message(models.Model):

    roles = [
        ('organization', 'University/organization'),
        ('participant', 'Participant'),
        ('coach', 'Coach'),
        ('referee', 'Referee')
    ]

    created_at = models.DateTimeField(default=timezone.now, verbose_name=_('Creation Date'))
    date_published = models.DateTimeField(auto_now_add=True, verbose_name=_('Publication Date'))
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=_('Author'))
    text = models.TextField(verbose_name=_('Text'))
    recipient = models.CharField(max_length=15, choices=roles, default='participant', verbose_name=_('Recipient'))
    documents = models.ManyToManyField('Document', verbose_name=_('Documents'))

    def __str__(self):
        return f"Message by {self.author} - {self.created_at}"


class Event(models.Model):

    types = [('registration', 'Registration of participants'), ('document_upload', 'Document upload'),
             ('online_conference', 'Online conference'), ('summarizing', 'Summarizing')]

    created_at = models.DateTimeField(default=timezone.now, verbose_name=_('Creation Date'))
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=_('Author'))
    start_date = models.DateTimeField(verbose_name=_('Start'))
    end_date = models.DateTimeField(null=True, blank=True, verbose_name=_('End'))
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    description = models.TextField(verbose_name=_('Description'))
    event_type = models.CharField(max_length=50, choices=types, verbose_name=_('Event type'))
    file = models.ManyToManyField('Document', blank=True, verbose_name=_('Documents'))
    scheduled_video_conference_url = models.URLField(null=True, blank=True, verbose_name=_('Videoconference'))
    online_stream_url = models.URLField(null=True, blank=True, verbose_name=_('Stream'))

    def __str__(self):
        return self.title


class Channel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_('Creation Date'))
