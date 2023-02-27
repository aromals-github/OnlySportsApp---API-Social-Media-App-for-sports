# Generated by Django 4.1.3 on 2023-02-25 18:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cricket', '0002_tournament_notifications'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tournament_Reports',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reporters', models.ManyToManyField(blank=True, related_name='reporters', to=settings.AUTH_USER_MODEL)),
                ('tournament', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='cricket.hostcrickettournaments')),
            ],
        ),
    ]
