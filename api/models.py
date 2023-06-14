from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import UniqueConstraint

from .configs import MEASUREMENT_UNIT
from .validators import positive_number, validate_less_hundred, \
    validate_hex_color

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


class Promotion(models.Model):
    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'

    name = models.CharField(
        'Название',
        max_length=255,
    )
    hex_color = models.CharField(
        'Цвет акции',
        max_length=16,
        validators=[validate_hex_color],
    )

    def __str__(self):
        return self.name


class Product(TimeBasedModel):
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']

    kind = models.CharField(
        'Разновидность',
        max_length=50,
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
        default=0,
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
        return f'{self.kind} - {self.name}'


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


# Модели для Collection
class Collection(TimeBasedModel):
    class Meta:
        verbose_name = 'Коллекция'
        verbose_name_plural = 'Коллекции'
        ordering = ['kind']

    kind = models.CharField(
        'Разновидность',
        max_length=50,
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
        default=0,
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
    promotion = models.ForeignKey(
        Promotion,
        on_delete=models.SET_NULL,
        related_name='collections',
        null=True,
        blank=True,
    )
    price = models.IntegerField(
        'Цена',
        validators=[positive_number],
    )
    product = models.ManyToManyField(
        Product,
        through='CollectionProduct',
        verbose_name='Товар',
    )
    property = models.ManyToManyField(
        Property,
        through='CollectionProperty',
    )
    image = models.ImageField(
        'Картинка',
        upload_to='products/images/',
        blank=True,
    )


class CollectionProduct(models.Model):
    collection = models.ForeignKey(
        Collection,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Коллекция',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='collections',
        verbose_name='Товар',
    )
    is_full = models.BooleanField(
        'Полный товар',
        default=True,
    )


class CollectionProperty(models.Model):
    class Meta:
        verbose_name = 'Коллекция - Свойство'
        verbose_name_plural = 'Коллекции - Свойства'
        constraints = [
            UniqueConstraint(
                fields=('collection', 'property'),
                name='unique_collection_property',
            ),
        ]

    collection = models.ForeignKey(
        Collection,
        on_delete=models.CASCADE,
        related_name='properties',
        verbose_name='Коллекция',
    )
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='collections',
        verbose_name='Свойство',
    )

    def __str__(self):
        return f'{self.collection} - {self.property}'


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


# Акции
class Sale(models.Model):
    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'

    image = models.ImageField(
        upload_to='sales/images/'
    )
