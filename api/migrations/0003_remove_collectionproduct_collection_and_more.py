# Generated by Django 4.2.2 on 2023-06-16 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_banner_category_categorybanner_city_collection_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collectionproduct',
            name='collection',
        ),
        migrations.RemoveField(
            model_name='collectionproduct',
            name='product',
        ),
        migrations.RemoveField(
            model_name='collectionproperty',
            name='collection',
        ),
        migrations.RemoveField(
            model_name='collectionproperty',
            name='property',
        ),
        migrations.AlterModelOptions(
            name='collection',
            options={},
        ),
        migrations.RemoveField(
            model_name='collection',
            name='calorie',
        ),
        migrations.RemoveField(
            model_name='collection',
            name='carbohydrates',
        ),
        migrations.RemoveField(
            model_name='collection',
            name='category',
        ),
        migrations.RemoveField(
            model_name='collection',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='collection',
            name='description',
        ),
        migrations.RemoveField(
            model_name='collection',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='collection',
            name='fats',
        ),
        migrations.RemoveField(
            model_name='collection',
            name='image',
        ),
        migrations.RemoveField(
            model_name='collection',
            name='name',
        ),
        migrations.RemoveField(
            model_name='collection',
            name='price',
        ),
        migrations.RemoveField(
            model_name='collection',
            name='product',
        ),
        migrations.RemoveField(
            model_name='collection',
            name='promotion',
        ),
        migrations.RemoveField(
            model_name='collection',
            name='property',
        ),
        migrations.RemoveField(
            model_name='collection',
            name='proteins',
        ),
        migrations.RemoveField(
            model_name='collection',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='collection',
            name='child_product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='parents', to='api.product'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='collection',
            name='parent_product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='components', to='api.product'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='collection',
            field=models.ManyToManyField(through='api.Collection', to='api.product'),
        ),
        migrations.DeleteModel(
            name='CollectionCategory',
        ),
        migrations.DeleteModel(
            name='CollectionProduct',
        ),
        migrations.DeleteModel(
            name='CollectionProperty',
        ),
    ]
