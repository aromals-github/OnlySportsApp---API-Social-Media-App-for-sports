# Generated by Django 4.1.3 on 2023-03-04 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team_management', '0004_remove_clubregisteredfootballtournament_club_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='clubcricketmembers',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
