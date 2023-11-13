from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Tag(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Tag'))

    def __str__(self):
        return self.name

