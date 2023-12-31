# Generated by Django 4.2.6 on 2023-10-19 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contest', '0001_initial'),
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mootcourt',
            name='documents',
            field=models.ManyToManyField(to='service.document', verbose_name='Documents'),
        ),
        migrations.AddField(
            model_name='mootcourt',
            name='events',
            field=models.ManyToManyField(to='service.event', verbose_name='Events'),
        ),
        migrations.AddField(
            model_name='mootcourt',
            name='messages',
            field=models.ManyToManyField(blank=True, to='service.message', verbose_name='Messages'),
        ),
    ]
