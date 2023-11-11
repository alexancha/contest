from django.utils import timezone

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class ProfileManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, password, **extra_fields)


# Определите модель пользователя
class Profile(AbstractBaseUser, PermissionsMixin):

    roles = [
        ('organization', 'University/organization'),
        ('participant', 'Participant'),
        ('coach', 'Coach'),
        ('referee', 'Referee')
    ]
    Status = [
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ]
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_('Creation Date'))
    first_name = models.CharField(max_length=255, verbose_name=_('Name'))
    position = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Position'))
    photo = models.ImageField(upload_to='user_photos/', null=True, blank=True, verbose_name=_('Photo'))
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))
    university_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('University'))
    university_link = models.URLField(null=True, blank=True, verbose_name=_('University link'))
    accept_team_invitations = models.BooleanField(default=False, verbose_name=_('Accept team invitation'))
    verified_user = models.BooleanField(default=False, verbose_name=_('Verified user'))
    rating = models.FloatField(null=True, blank=True, verbose_name=_('Rating'))
    email = models.EmailField(unique=True, verbose_name=_('Email'))
    phone = models.CharField(max_length=20, verbose_name=_('Phone number'))
    role = models.CharField(max_length=15, choices=roles, verbose_name=_('Role'))
    status = models.CharField(max_length=8, choices=Status, default='inactive', verbose_name=_('Status'))
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = ProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.first_name


class AdminProfile(Profile):
    class Meta:
        proxy = True
        verbose_name = "Admin"
        verbose_name_plural = "Admins"


class OrganizationProfile(Profile):
    class Meta:
        proxy = True
        verbose_name = "University/Organization"
        verbose_name_plural = "Universities/Organizations"


class ParticipantProfile(Profile):
    class Meta:
        proxy = True
        verbose_name = "Participant"
        verbose_name_plural = "Participants"


class Team(models.Model):

    Status = [
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ]

    created_at = models.DateTimeField(default=timezone.now, verbose_name=_('Creation Date'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))
    logo = models.ImageField(upload_to='team_logos/', null=True, blank=True, verbose_name=_('Logo'))
    organization = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                     related_name='organizations', verbose_name=_('Organization'))
    verified_by_organization = models.BooleanField(default=False, verbose_name=_('Verified by organization'))
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='owned_teams', verbose_name=_('Owner'))
    captain = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True,
                                related_name='captain_of_teams', verbose_name=_('Captain'))
    coaches = models.ManyToManyField(Profile, related_name='teams_coached', verbose_name=_('Coaches'))
    members = models.ManyToManyField(Profile, related_name='teams_as_member', verbose_name=_('Members'))
    rating = models.FloatField(null=True, blank=True, verbose_name=_('Rating'))
    status = models.CharField(max_length=8, choices=Status, default='inactive', verbose_name=_('Status'))

    def __str__(self):
        return self.name