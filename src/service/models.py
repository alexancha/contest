from django.db import models
from contest.models import  Mootcourt
from users.models import CustomUser


class Teaser(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    publication_date = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    background = models.CharField(max_length=255)
    image = models.URLField()
    link = models.URLField()
    mootcourt = models.ForeignKey(Mootcourt, on_delete=models.CASCADE, related_name='teasers')

    def __str__(self):
        return self.title


class Document(models.Model):

    types = ['Fabula', 'Reglament', 'File', 'Procedural Document', 'Result of moot court']

    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=5, choices=types)
    file_name = models.CharField(max_length=255)
    icon = models.FileField(upload_to='icons/')
    file = models.FileField(upload_to='documents/')


class Message(models.Model):

    roles = [
        ('Organ', 'University/organization'),
        ('Part', 'Participant'),
        ('Coach', 'Coach'),
        ('Ref', 'Referee')
    ]

    date_created = models.DateTimeField(auto_now_add=True)
    date_published = models.DateTimeField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    recipient = models.CharField(max_length=5, choices=roles, default='Part')
    documents = models.ManyToManyField('Document', blank=True)

    def __str__(self):
        return f"Message by {self.author} - {self.date_created}"


class Event(models.Model):

    types = ['Registration of participants', 'Document upload',
             'Online conference', 'Summary or Conclusion']

    date_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    event_type = models.CharField(max_length=50, choices=types)
    file = models.ForeignKey('Document', null=True, blank=True,
                             on_delete=models.SET_NULL)
    scheduled_video_conference_url = models.URLField(null=True, blank=True)
    online_stream_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title
