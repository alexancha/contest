from django.db import models
from django.utils import timezone
from users.models import Profile, Team
from service.models import Message, Channel, Event, Document
from guides.models import Tag
from django.utils.translation import gettext_lazy as _


class Mootcourt(models.Model):
    Status = [
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ]
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_('Creation Date'))
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    organizer = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=_('Organizer'))
    event_type = models.CharField(max_length=7,
                                  choices=[('open', 'Open'), ('private', 'Private')],
                                  default='opened', verbose_name=_('Event Type'))
    # tags = models.ManyToManyField(Tag, blank=True,
    #                               limit_choices_to={'tags__count__lt': 50}, verbose_name=_('Tags'))
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=_('Tags'))
    announcement = models.TextField(verbose_name=_('Announcement'))
    messages = models.ManyToManyField(Message, blank=True, verbose_name=_('Messages'))
    events = models.ManyToManyField(Event, verbose_name=_('Events'))
    documents = models.ManyToManyField(Document, verbose_name=_('Documents'))
    need_telegram_channel = models.BooleanField(default=False, verbose_name=_('Need for TG channel'))
    telegram_channel = models.ForeignKey(Channel, on_delete=models.SET_NULL,
                                         null=True, verbose_name=_('Telegram Channel'))
    teams = models.ManyToManyField(Team, verbose_name=_('Teams'))
    senior_referees = models.ManyToManyField(Profile, related_name='senior_arbiters', verbose_name=_('Senior referees'))
    referees = models.ManyToManyField(Profile, related_name='arbiters', verbose_name=_('Referees'))
    status_moot_court = models.CharField(max_length=12,
                                         choices=[('registration', 'Registration'),
                                                  ('active', 'Active'),
                                                  ('completed', 'Completed')],
                                         verbose_name=_('Moot court status'))
    background = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Background'))
    image = models.ImageField(upload_to='mootkourt_images/', null=True, blank=True, verbose_name=_('Image'))
    status = models.CharField(max_length=8, choices=Status, default='inactive', verbose_name=_('Status'))
    display_on_main = models.BooleanField(default=True, verbose_name=_('Display on main page'))

    def __str__(self):
        return self.title
