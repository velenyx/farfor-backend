# Generated by Django 4.2.2 on 2023-06-15 08:39

import api.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70, verbose_name='Оглавление')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('slug', models.SlugField(default='', unique=True)),
                ('image', models.ImageField(upload_to='banners/images/', verbose_name='Картинка')),
            ],
            options={
                'verbose_name': 'Баннер',
                'verbose_name_plural': 'Баннеры',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(upload_to='categories/images/', verbose_name='Картинка')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='CategoryBanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='api.banner')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='banners', to='api.category')),
            ],
            options={
                'verbose_name': 'Категория - Баннер',
                'verbose_name_plural': 'Категории - Баннеры',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('name', models.CharField(max_length=70, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('discount', models.IntegerField(default=0, validators=[django.core.validators.RegexValidator(message='Число должно быть положительным', regex='^[0-9]+$'), api.validators.validate_less_hundred], verbose_name='Скидка')),
                ('calorie', models.IntegerField(blank=True, null=True, validators=[django.core.validators.RegexValidator(message='Число должно быть положительным', regex='^[0-9]+$')], verbose_name='Калории')),
                ('proteins', models.IntegerField(blank=True, null=True, validators=[django.core.validators.RegexValidator(message='Число должно быть положительным', regex='^[0-9]+$')], verbose_name='Белки')),
                ('fats', models.IntegerField(blank=True, null=True, validators=[django.core.validators.RegexValidator(message='Число должно быть положительным', regex='^[0-9]+$')], verbose_name='Жиры')),
                ('carbohydrates', models.IntegerField(blank=True, null=True, validators=[django.core.validators.RegexValidator(message='Число должно быть положительным', regex='^[0-9]+$')], verbose_name='Углероды')),
                ('price', models.IntegerField(validators=[django.core.validators.RegexValidator(message='Число должно быть положительным', regex='^[0-9]+$')], verbose_name='Цена')),
                ('image', models.ImageField(blank=True, upload_to='products/images/', verbose_name='Картинка')),
            ],
            options={
                'verbose_name': 'Коллекция',
                'verbose_name_plural': 'Коллекции',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='CollectionCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collections', to='api.category')),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='api.collection')),
            ],
            options={
                'verbose_name': 'Коллекция - Категория',
                'verbose_name_plural': 'Коллекции - Категории',
            },
        ),
        migrations.CreateModel(
            name='CollectionProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_full', models.BooleanField(default=True, verbose_name='Полный товар')),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='api.collection', verbose_name='Коллекция')),
            ],
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
            name='Condition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Условие',
                'verbose_name_plural': 'Условия',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70, unique=True, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Страна',
                'verbose_name_plural': 'Страны',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='api.category')),
            ],
            options={
                'verbose_name': 'Товар - Категория',
                'verbose_name_plural': 'Товары - Категории',
            },
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Название')),
                ('title', models.CharField(max_length=255, verbose_name='Загаловок')),
                ('description', models.TextField(verbose_name='Описание')),
                ('slug', models.SlugField(default='', unique=True)),
                ('hex_color', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(message='Неправильный формат цвета', regex='^#[a-zA-Z0-9]+$')], verbose_name='Цвет акции')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='Дата начала акции')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='Дата конца акции')),
                ('image', models.ImageField(upload_to='promotions/images/', verbose_name='Картинка')),
            ],
            options={
                'verbose_name': 'Акция',
                'verbose_name_plural': 'Акции',
            },
        ),
        migrations.CreateModel(
            name='PromotionCondition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='promotions', to='api.condition')),
                ('promotion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conditions', to='api.promotion')),
            ],
            options={
                'verbose_name': 'Акция - условие',
                'verbose_name_plural': 'Акции - условия',
            },
        ),
        migrations.DeleteModel(
            name='Location',
        ),
        migrations.RemoveField(
            model_name='product',
            name='kind',
        ),
        migrations.AlterField(
            model_name='productproperty',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to='api.product', verbose_name='Товар'),
        ),
        migrations.AddField(
            model_name='promotion',
            name='condition',
            field=models.ManyToManyField(through='api.PromotionCondition', to='api.condition'),
        ),
        migrations.AddField(
            model_name='productcategory',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='api.product'),
        ),
        migrations.AddField(
            model_name='collectionproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collections', to='api.product', verbose_name='Товар'),
        ),
        migrations.AddField(
            model_name='collection',
            name='category',
            field=models.ManyToManyField(through='api.CollectionCategory', to='api.category', verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='collection',
            name='product',
            field=models.ManyToManyField(through='api.CollectionProduct', to='api.product', verbose_name='Товар'),
        ),
        migrations.AddField(
            model_name='collection',
            name='promotion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='collections', to='api.promotion'),
        ),
        migrations.AddField(
            model_name='collection',
            name='property',
            field=models.ManyToManyField(through='api.CollectionProperty', to='api.property'),
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='api.country', verbose_name='Страна'),
        ),
        migrations.AddField(
            model_name='category',
            name='banner',
            field=models.ManyToManyField(through='api.CategoryBanner', to='api.banner', verbose_name='Баннер'),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(through='api.ProductCategory', to='api.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='product',
            name='promotion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='api.promotion'),
        ),
        migrations.AddConstraint(
            model_name='collectionproperty',
            constraint=models.UniqueConstraint(fields=('collection', 'property'), name='unique_collection_property'),
        ),
        migrations.AddConstraint(
            model_name='city',
            constraint=models.UniqueConstraint(fields=('name', 'country'), name='unique_location'),
        ),
    ]
