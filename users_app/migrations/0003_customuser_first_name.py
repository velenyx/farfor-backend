# Generated by Django 4.2.2 on 2023-06-09 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0002_alter_customuser_date_of_birth_alter_customuser_sex'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(max_length=255, null=True, verbose_name='Имя'),
        ),
    ]