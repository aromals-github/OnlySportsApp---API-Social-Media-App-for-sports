# Generated by Django 4.1.3 on 2022-12-15 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cricket', '0008_alter_postfuntions_report'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postfuntions',
            name='report',
            field=models.CharField(choices=[(2, 'This post is not related to cricket'), (3, 'Content of the this particualr post is abusive'), (4, 'Sexual Content '), (5, 'Others')], default=1, max_length=60),
        ),
    ]
