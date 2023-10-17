from .models import Teaser
from contest.models import Mootcourt
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Mootcourt)
def create_mootcourt_teaser(sender, instance, created, **kwargs):
    if created:
        Teaser.objects.create(title=instance.title, mootcourt=instance, description=instance.description,
                              background=instance.background, image_url="", link="")
