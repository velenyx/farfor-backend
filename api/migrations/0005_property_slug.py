# Generated by Django 4.2.2 on 2023-06-21 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_property_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='slug',
            field=models.SlugField(default='', unique=True),
        ),
    ]
