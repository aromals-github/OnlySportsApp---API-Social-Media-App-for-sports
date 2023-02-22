# Generated by Django 4.1.3 on 2023-02-17 05:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clubs', '0009_membershipresponses_waiting'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membershipresponses',
            name='declined',
        ),
        migrations.AddField(
            model_name='membershipresponses',
            name='blocked',
            field=models.ManyToManyField(blank=True, related_name='blocked', to=settings.AUTH_USER_MODEL),
        ),
    ]