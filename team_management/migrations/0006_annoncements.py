# Generated by Django 4.1.3 on 2023-03-18 08:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0003_remove_clubhistoryperuser_club_admin_of'),
        ('team_management', '0005_clubcricketmembers_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Annoncements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=600)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clubs.clubs')),
            ],
            options={
                'verbose_name_plural': 'Annocements',
            },
        ),
    ]
