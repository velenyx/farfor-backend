# Generated by Django 4.2.2 on 2023-06-16 15:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_collection_is_full_alter_category_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='child_product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='parents', to='api.product', verbose_name='Товар'),
            preserve_default=False,
        ),
    ]
