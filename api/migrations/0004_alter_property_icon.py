# Generated by Django 4.2.2 on 2023-06-21 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_product_calorie_alter_product_carbohydrates_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='icon',
            field=models.FileField(blank=True, null=True, upload_to='properties/images/', verbose_name='Иконка'),
        ),
    ]
