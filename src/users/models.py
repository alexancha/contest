from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


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

        return self.create_user(email, password, **extra_fields)


# Определите модель пользователя
class Profile(AbstractBaseUser, PermissionsMixin):

    roles = [
        ('organization', 'University/organization'),
        ('participant', 'Participant'),
        ('coach', 'Coach'),
        ('referee', 'Referee')
    ]

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    first_name = models.CharField(max_length=255, verbose_name=_('First name'))
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
    role = models.CharField(max_length=15, choices=roles, default='participant', verbose_name=_('Role'))
    status = models.CharField(max_length=8, default='Inactive', verbose_name=_('Status'))
    is_staff = models.BooleanField(default=False)

    objects = ProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


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


class Team(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True,)
    logo = models.ImageField(upload_to='team_logos/', null=True, blank=True,)
    organization = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='organizations')
    verified_by_organization = models.BooleanField(default=False)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='owned_teams')
    captain = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='captain_of_teams')
    coaches = models.ManyToManyField(Profile, related_name='teams_coached')
    members = models.ManyToManyField(Profile, related_name='teams_as_member')
    rating = models.FloatField(null=True, blank=True,)
    status = models.CharField(max_length=8, default='Inactive')

    def __str__(self):
        return self.name