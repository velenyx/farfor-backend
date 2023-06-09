from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import UniqueConstraint

from .configs import MEASUREMENT_UNIT
from .validators import positive_number, validate_less_hundred

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
    promotion = models.CharField(
        'Акция',
        max_length=100,
        null=True,
        blank=True,
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
        return self.name


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


# Модели для Location
class Location(models.Model):
    class Meta:
        verbose_name = ''
