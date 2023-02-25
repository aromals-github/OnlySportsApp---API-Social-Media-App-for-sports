# Generated by Django 4.1.3 on 2023-02-25 15:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clubs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HostCricketTournaments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tournament_name', models.CharField(blank=True, max_length=70, null=True)),
                ('banner', models.ImageField(blank=True, null=True, upload_to='CricketTournaments')),
                ('district', models.CharField(blank=True, choices=[('AL', 'Alappuzha'), ('ER', 'Ernakulam'), ('ID', 'Idukki'), ('KN', 'Kannur'), ('KS', 'Kasaragod'), ('KL', 'Kollam'), ('KT', 'Kottayam'), ('KZ', 'Kozhikode'), ('MA', 'Malapuram'), ('PL', 'Palakkad'), ('PT', 'Pathanmthitta'), ('TV', 'Thiruvanathapuram'), ('TS', 'Thirssur'), ('WA', 'Wayanad')], max_length=2, null=True)),
                ('venue', models.CharField(blank=True, max_length=70, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(blank=True, max_length=1000, null=True)),
                ('date', models.DateField(null=True)),
                ('limit_participants', models.IntegerField(blank=True, null=True)),
                ('contact', models.CharField(blank=True, max_length=600, null=True)),
                ('end_registration', models.DateField(blank=True, null=True)),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('registered_teams', models.ManyToManyField(blank=True, related_name='Registered', to='clubs.clubs')),
            ],
            options={
                'verbose_name': 'Cricket Tournament',
                'verbose_name_plural': 'Cricket Tournaments',
            },
        ),
    ]
