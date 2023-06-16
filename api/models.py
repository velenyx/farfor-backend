from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import UniqueConstraint

from .configs import MEASUREMENT_UNIT
from .validators import (
    positive_number,
    validate_less_hundred,
    validate_hex_color,
)

User = get_user_model()


class TimeBasedModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        'Дата обновления',
        auto_now=True,
    )


# Модели для товара
class Property(models.Model):
    class Meta:
        verbose_name = 'Свойство'
        verbose_name_plural = 'Свойства'

    name = models.CharField(
        'Название',
        max_length=20,
    )
    icon = models.FileField(
        'Иконка',
        upload_to='properties/images/',
    )

    def __str__(self):
        return self.name


class Size(models.Model):
    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'
        constraints = [
            UniqueConstraint(
                fields=('size', 'measurement'),
                name='unique_size',
            ),
        ]

    size = models.IntegerField(
        'Размер',
        validators=[positive_number]
    )
    measurement = models.CharField(
        'Единица измерения',
        choices=MEASUREMENT_UNIT,
        max_length=2,
    )

    def __str__(self):
        return f'{self.size}{self.measurement}'


class Condition(models.Model):
    class Meta:
        verbose_name = 'Условие'
        verbose_name_plural = 'Условия'

    name = models.CharField(
        'Название',
        max_length=255,
    )

    def __str__(self):
        return self.name


class Promotion(models.Model):
    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'

    name = models.CharField(
        'Название',
        max_length=255,
        null=True,
        blank=True,
    )
    title = models.CharField(
        'Загаловок',
        max_length=255,
    )
    description = models.TextField(
        'Описание',
    )
    slug = models.SlugField(
        unique=True,
        null=False,
        default="",
    )
    hex_color = models.CharField(
        'Цвет акции',
        max_length=16,
        validators=[validate_hex_color],
    )
    start_date = models.DateField(
        'Дата начала акции',
        null=True,
        blank=True,
    )
    end_date = models.DateField(
        'Дата конца акции',
        null=True,
        blank=True,
    )
    image = models.ImageField(
        'Картинка',
        upload_to='promotions/images/',
    )
    condition = models.ManyToManyField(
        Condition,
        through='PromotionCondition',
    )

    def __str__(self):
        return self.name


class PromotionCondition(models.Model):
    class Meta:
        verbose_name = 'Акция - условие'
        verbose_name_plural = 'Акции - условия'

    promotion = models.ForeignKey(
        Promotion,
        on_delete=models.CASCADE,
        related_name='conditions',
    )
    condition = models.ForeignKey(
        Condition,
        on_delete=models.CASCADE,
        related_name='promotions',
    )


class Banner(models.Model):
    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'

    title = models.CharField(
        'Оглавление',
        max_length=70,
    )
    description = models.TextField(
        'Описание',
        null=True,
        blank=True,
    )
    slug = models.SlugField(
        unique=True,
        null=False,
        default='',
    )
    image = models.ImageField(
        'Картинка',
        upload_to='banners/images/',
    )

    def __str__(self):
        return self.title


class Category(TimeBasedModel):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['created_at']

    name = models.CharField(
        'Название',
        max_length=255,
    )
    description = models.TextField(
        'Описание',
        null=True,
        blank=True,
    )
    slug = models.SlugField(
        unique=True,
    )
    image = models.ImageField(
        'Картинка',
        upload_to='categories/images/',
    )
    banner = models.ManyToManyField(
        Banner,
        through='CategoryBanner',
        verbose_name='Баннер',
    )

    def __str__(self):
        return self.name


class CategoryBanner(models.Model):
    class Meta:
        verbose_name = 'Категория - Баннер'
        verbose_name_plural = 'Категории - Баннеры'

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='banners',
    )
    banner = models.ForeignKey(
        Banner,
        on_delete=models.CASCADE,
        related_name='categories',
    )


class Product(TimeBasedModel):
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']

    category = models.ManyToManyField(
        Category,
        through='ProductCategory',
        verbose_name='Категория',
    )
    name = models.CharField(
        'Название',
        max_length=70,
    )
    description = models.TextField(
        'Описание',
    )
    discount = models.IntegerField(
        'Скидка',
        validators=[positive_number, validate_less_hundred],
        null=True,
        blank=True,
    )
    calorie = models.IntegerField(
        'Калории',
        validators=[positive_number],
        null=True,
        blank=True,
    )
    proteins = models.IntegerField(
        'Белки',
        validators=[positive_number],
        null=True,
        blank=True,
    )
    fats = models.IntegerField(
        'Жиры',
        validators=[positive_number],
        null=True,
        blank=True,
    )
    carbohydrates = models.IntegerField(
        'Углероды',
        validators=[positive_number],
        null=True,
        blank=True,
    )
    collection = models.ManyToManyField(
        "self",
        through='Collection',
    )
    promotion = models.ForeignKey(
        Promotion,
        on_delete=models.SET_NULL,
        related_name='products',
        null=True,
        blank=True,
    )
    size = models.ManyToManyField(
        Size,
        through='ProductSize',
        verbose_name='Размеры',
    )
    property = models.ManyToManyField(
        Property,
        through='ProductProperty',
    )
    image = models.ImageField(
        'Картинка',
        upload_to='products/images/',
        blank=True,
    )

    def __str__(self):
        return f'{self.category} - {self.name}'


class ProductCategory(models.Model):
    class Meta:
        verbose_name = 'Товар - Категория'
        verbose_name_plural = 'Товары - Категории'

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='categories',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Категория',
    )


class ProductProperty(models.Model):
    class Meta:
        verbose_name = 'Продукт - Свойство'
        verbose_name_plural = 'Продукты - Свойства'
        constraints = [
            UniqueConstraint(
                fields=('product', 'property'),
                name='unique_product_property',
            ),
        ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='properties',
        verbose_name='Товар',
    )
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Свойство',
    )

    def __str__(self):
        return f'{self.product} - {self.property}'


class ProductSize(models.Model):
    class Meta:
        verbose_name = 'Тип товара'
        verbose_name_plural = 'Типы товаров'

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='sizes',
    )
    size = models.ForeignKey(
        Size,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Размер',
    )
    price = models.IntegerField(
        'Цена',
        validators=[positive_number],
    )
    weight = models.IntegerField(
        'Вес',
        validators=[positive_number],
    )

    def __str__(self):
        return f'{self.product} - {self.size}'


class Collection(models.Model):
    class Meta:
        verbose_name = 'Коллекция'
        verbose_name_plural = 'Коллекции'
        constraints = [
            UniqueConstraint(
                fields=('parent_product', 'child_product'),
                name='unique_collection',
            ),
        ]

    parent_product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='components',
    )
    child_product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='parents',
        verbose_name='Товар',
    )
    is_full = models.BooleanField(
        default=True,
    )


# Модели для Location
class Country(models.Model):
    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
        ordering = ('name',)

    name = models.CharField(
        'Название',
        max_length=70,
        unique=True,
    )

    def __str__(self):
        return self.name


class City(models.Model):
    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ('name',)
        constraints = [
            UniqueConstraint(
                fields=('name', 'country'),
                name='unique_location',
            ),
        ]

    name = models.CharField(
        'Название',
        max_length=70,
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name='cities',
        verbose_name='Страна',
    )

    def __str__(self):
        return f'{self.country} - {self.name}'
