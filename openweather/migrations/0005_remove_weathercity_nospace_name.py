# Generated by Django 3.0 on 2020-01-19 01:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('openweather', '0004_weathercity_api_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weathercity',
            name='nospace_name',
        ),
    ]
