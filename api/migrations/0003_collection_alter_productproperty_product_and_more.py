# Generated by Django 4.2.2 on 2023-06-10 14:56

import api.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_promotion_alter_product_promotion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('kind', models.CharField(max_length=50, verbose_name='Разновидность')),
                ('name', models.CharField(max_length=70, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('discount', models.IntegerField(default=0, validators=[django.core.validators.RegexValidator(message='Число должно быть положительным', regex='^[0-9]+$'), api.validators.validate_less_hundred], verbose_name='Скидка')),
                ('calorie', models.IntegerField(blank=True, null=True, validators=[django.core.validators.RegexValidator(message='Число должно быть положительным', regex='^[0-9]+$')], verbose_name='Калории')),
                ('proteins', models.IntegerField(blank=True, null=True, validators=[django.core.validators.RegexValidator(message='Число должно быть положительным', regex='^[0-9]+$')], verbose_name='Белки')),
                ('fats', models.IntegerField(blank=True, null=True, validators=[django.core.validators.RegexValidator(message='Число должно быть положительным', regex='^[0-9]+$')], verbose_name='Жиры')),
                ('carbohydrates', models.IntegerField(blank=True, null=True, validators=[django.core.validators.RegexValidator(message='Число должно быть положительным', regex='^[0-9]+$')], verbose_name='Углероды')),
                ('price', models.IntegerField(validators=[django.core.validators.RegexValidator(message='Число должно быть положительным', regex='^[0-9]+$')], verbose_name='Цена')),
                ('weight', models.IntegerField(validators=[django.core.validators.RegexValidator(message='Число должно быть положительным', regex='^[0-9]+$')], verbose_name='Вес')),
                ('image', models.ImageField(blank=True, upload_to='products/images/', verbose_name='Картинка')),
            ],
            options={
                'verbose_name': 'Коллекция',
                'verbose_name_plural': 'Коллекции',
            },
        ),
        migrations.AlterField(
            model_name='productproperty',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to='api.product', verbose_name='Товар'),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='hex_color',
            field=models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(message='Неправильный формат цвета', regex='^#[a-zA-Z0-9]+$')], verbose_name='Цвет акции'),
        ),
        migrations.CreateModel(
            name='CollectionProperty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to='api.collection', verbose_name='Коллекция')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collections', to='api.property', verbose_name='Свойство')),
            ],
            options={
                'verbose_name': 'Коллекция - Свойство',
                'verbose_name_plural': 'Коллекции - Свойства',
            },
        ),
        migrations.CreateModel(
            name='CollectionProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='api.collection', verbose_name='Коллекция')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collections', to='api.product', verbose_name='Товар')),
            ],
        ),
        migrations.AddField(
            model_name='collection',
            name='product',
            field=models.ManyToManyField(through='api.CollectionProduct', to='api.product', verbose_name='Товар'),
        ),
        migrations.AddField(
            model_name='collection',
            name='promotion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='collections', to='api.promotion'),
        ),
        migrations.AddField(
            model_name='collection',
            name='property',
            field=models.ManyToManyField(through='api.CollectionProperty', to='api.property'),
        ),
        migrations.AddConstraint(
            model_name='collectionproperty',
            constraint=models.UniqueConstraint(fields=('collection', 'property'), name='unique_collection_property'),
        ),
    ]