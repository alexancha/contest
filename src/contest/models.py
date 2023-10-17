from django.db import models
from users.models import CustomUser, Team
from service.models import *


class Mootcourt(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    organizer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    premut = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    event_type = models.CharField(max_length=6, choices=['opened', 'closed'], default='opened')
    tags = models.ManyToManyField(Tag, blank=True, limit_choices_to={'tags__count__lt': 50})
    announcement = models.TextField()
    messages = models.ManyToManyField('Message', blank=True)
    events = models.ManyToManyField(Event)
    documents = models.ManyToManyField(Document, limit_choices_to={'name__in': ['Фабула']})
    need_telegram_channel = models.BooleanField()
    telegram_channel = models.OneToOneField('Channel', on_delete=models.CASCADE)
    teams = models.ManyToManyField(Team, blank=True)
    senior_arbiters = models.ManyToManyField(CustomUser, related_name='senior_arbiters', blank=True)
    arbiters = models.ManyToManyField(CustomUser, related_name='arbiters', blank=True)
    status = models.CharField(max_length=12, choices=['registration', 'active', 'completed'])
    background = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='mootkourt_images/', blank=True)
    teaser = models.OneToOneField(Teaser, on_delete=models.SET_NULL, null=True, blank=True)
    display_on_main = models.BooleanField(default=True)

    def __str__(self):
        return self.title
