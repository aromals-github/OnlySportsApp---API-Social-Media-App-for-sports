# Generated by Django 4.1.3 on 2022-12-07 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cricket', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cricketposts',
            options={'verbose_name_plural': 'cricket posts'},
        ),
        migrations.AddField(
            model_name='cricketposts',
            name='report',
            field=models.CharField(choices=[('FR', 'Freshman'), ('SO', 'Sophomore'), ('JR', 'Junior'), ('SR', 'Senior'), ('GR', 'Graduate')], default=None, max_length=30),
        ),
    ]
