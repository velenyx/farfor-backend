# Generated by Django 4.2.2 on 2023-06-10 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_product_is_full'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_full',
        ),
        migrations.AddField(
            model_name='collectionproduct',
            name='is_full',
            field=models.BooleanField(default=True, verbose_name='Полный товар'),
        ),
    ]