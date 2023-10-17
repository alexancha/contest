from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import FileExtensionValidator
from django.urls import reverse


# Создайте менеджер пользователя
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


# Определите модель пользователя
class CustomUser(AbstractBaseUser):

    roles = [
        ('Organ', 'University/organization'),
        ('Part', 'Participant'),
        ('Coach', 'Coach'),
        ('Ref', 'Referee')
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(upload_to='user_photos/', blank=True)
    description = models.TextField(blank=True)
    university_name = models.CharField(max_length=255, blank=True)
    university_link = models.URLField(blank=True)
    accept_team_invitations = models.BooleanField(default=False)
    verified_user = models.BooleanField(default=False)
    rating = models.FloatField(null=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    role = models.CharField(max_length=5, choices=roles, default='Part')
    status = models.CharField(max_length=8, default='Inactive')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.first_name


class Team(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='team_logos/', blank=True, null=True)
    organization = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='organizations')
    verified_by_organization = models.BooleanField(default=False)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='owned_teams')
    captain = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='captain_of_teams')
    coaches = models.ManyToManyField(CustomUser, related_name='teams_coached', blank=True)
    members = models.ManyToManyField(CustomUser, related_name='teams_as_member', blank=True)
    rating = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=8, default='Inactive')

    def __str__(self):
        return self.name