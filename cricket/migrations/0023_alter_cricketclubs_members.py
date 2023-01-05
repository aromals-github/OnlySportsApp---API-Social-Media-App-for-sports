# Generated by Django 4.1.3 on 2023-01-05 08:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cricket', '0022_alter_cricketclubs_members'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cricketclubs',
            name='members',
            field=models.ManyToManyField(blank=True, error_messages={'max-limit': 'max of 30 members'}, related_name='members', to=settings.AUTH_USER_MODEL),
        ),
    ]
