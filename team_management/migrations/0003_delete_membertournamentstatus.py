# Generated by Django 4.1.3 on 2023-03-03 17:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('team_management', '0002_alter_memberstatus_options_membertournamentstatus_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MemberTournamentStatus',
        ),
    ]
