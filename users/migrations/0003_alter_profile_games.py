# Generated by Django 4.1.3 on 2022-12-16 06:17

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_accounts_name_profile_bio_profile_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='games',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('C', 'Cricket'), ('F', 'Football'), ('G', 'General')], default='G', max_length=5),
        ),
    ]
