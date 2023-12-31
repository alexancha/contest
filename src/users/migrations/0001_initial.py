# Generated by Django 4.2.6 on 2023-10-19 16:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')),
                ('first_name', models.CharField(max_length=255, verbose_name='First name')),
                ('position', models.CharField(blank=True, max_length=255, null=True, verbose_name='Position')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='user_photos/', verbose_name='Photo')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('university_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='University')),
                ('university_link', models.URLField(blank=True, null=True, verbose_name='University link')),
                ('accept_team_invitations', models.BooleanField(default=False, verbose_name='Accept team invitation')),
                ('verified_user', models.BooleanField(default=False, verbose_name='Verified user')),
                ('rating', models.FloatField(blank=True, null=True, verbose_name='Rating')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('phone', models.CharField(max_length=20, verbose_name='Phone number')),
                ('role', models.CharField(choices=[('organization', 'University/organization'), ('participant', 'Participant'), ('coach', 'Coach'), ('referee', 'Referee')], default='participant', max_length=15, verbose_name='Role')),
                ('status', models.CharField(default='Inactive', max_length=8, verbose_name='Status')),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='team_logos/')),
                ('verified_by_organization', models.BooleanField(default=False)),
                ('rating', models.FloatField(blank=True, null=True)),
                ('status', models.CharField(default='Inactive', max_length=8)),
                ('captain', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='captain_of_teams', to=settings.AUTH_USER_MODEL)),
                ('coaches', models.ManyToManyField(related_name='teams_coached', to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(related_name='teams_as_member', to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organizations', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_teams', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AdminProfile',
            fields=[
            ],
            options={
                'verbose_name': 'Admin',
                'verbose_name_plural': 'Admins',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('users.profile',),
        ),
        migrations.CreateModel(
            name='OrganizationProfile',
            fields=[
            ],
            options={
                'verbose_name': 'University/Organization',
                'verbose_name_plural': 'Universities/Organizations',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('users.profile',),
        ),
    ]
