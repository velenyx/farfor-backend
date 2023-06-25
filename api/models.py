from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import UniqueConstraint

from .validators import (
    positive_number,
    validate_less_hundred,
    validate_hex_color, validate_less_ten,
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
    slug = models.SlugField(
        unique=True,
        null=False,
        default="",
    )
    icon = models.FileField(
        'Иконка',
        upload_to='properties/images/',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name


class KPFC(models.Model):
    class Meta:
        verbose_name = 'КБЖУ'
        verbose_name_plural = 'КБЖУ'

    calories = models.IntegerField(
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


class Modification(models.Model):
    class Meta:
        verbose_name = 'Модификация'
        verbose_name_plural = 'Модификации'

    name = models.CharField(
        'Название',
        max_length=255,
    )
    description = models.TextField(
        'Описание',
        null=True,
        blank=True,
    )
    mode = models.CharField(
        'Мод',
        null=True,
        blank=True,
    )
    amount = models.IntegerField(
        'Количество',
        null=True,
        blank=True,
    )
    price = models.IntegerField(
        'Цена',
        validators=[positive_number],
    )
    weight = models.IntegerField(
        'Вес',
        validators=[positive_number],
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


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
        null=True,
        blank=True,
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
        if self.name:
            return self.name
        return self.title


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
        null=True,
        blank=True,
    )
    discount = models.IntegerField(
        'Скидка',
        validators=[positive_number, validate_less_hundred],
        null=True,
        blank=True,
    )
    kpfc = models.ForeignKey(
        KPFC,
        on_delete=models.CASCADE,
        related_name='products',
    )
    component = models.ManyToManyField(
        Modification,
        through='Component',
        related_name='components',
        verbose_name='Компоненты',
    )
    promotion = models.ForeignKey(
        Promotion,
        on_delete=models.SET_NULL,
        related_name='products',
        null=True,
        blank=True,
    )
    modification = models.ManyToManyField(
        Modification,
        through='ProductModification',
        related_name='products',
        verbose_name='Модификации',
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


class ProductModification(models.Model):
    class Meta:
        verbose_name = 'Модификация - товар'
        verbose_name_plural = 'Модификации - товары'

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='modifications',
    )
    modification = models.ForeignKey(
        Modification,
        on_delete=models.CASCADE,
        verbose_name='Модификации',
    )

    def __str__(self):
        return f'{self.product} - {self.modification}'


class Component(models.Model):
    class Meta:
        verbose_name = 'Компонент'
        verbose_name_plural = 'Компоненты'
        constraints = [
            UniqueConstraint(
                fields=('product', 'modification'),
                name='unique_component',
            ),
        ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='components',
        verbose_name='Товар',
    )
    modification = models.ForeignKey(
        Modification,
        on_delete=models.CASCADE,
        verbose_name='Компоненты',
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


# Адрес
class Address(TimeBasedModel):
    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адресы'

    city = models.CharField(
        'Город',
        max_length=255,
        default='Липецк',
    )
    street = models.CharField(
        'Улица',
        max_length=255,
    )
    house = models.IntegerField(
        'Дом',
        validators=[positive_number],
    )
    apartment = models.IntegerField(
        'Квартира',
        validators=[positive_number],
        null=True,
        blank=True,
    )
    porch = models.IntegerField(
        'Подъезд',
        validators=[positive_number],
        null=True,
        blank=True,
    )
    floor = models.IntegerField(
        'Этаж',
        validators=[positive_number],
        null=True,
        blank=True,
    )
    intercom = models.IntegerField(
        'Домофон',
        validators=[positive_number],
        null=True,
        blank=True,
    )
    notes = models.TextField(
        'Комментарий',
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='addresses',
    )

    def __str__(self):
        return f'{self.city} - {self.street}., {self.house}'


# Доставка
class DeliveryKind(models.Model):
    class Meta:
        verbose_name = 'Разновидность доставки'
        verbose_name_plural = 'Разновидности доставки'

    price = models.FloatField(
        'Цена',
        default=0.0
    )
    message = models.CharField(
        'Сообщение',
        max_length=255,
    )
    status = models.CharField(
        'Статус доставки',
        max_length=255,
        default='FREE_DELIVERY'
    )

    def __str__(self):
        return f'{self.status} - {self.message}'


class Delivery(TimeBasedModel):
    class Meta:
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставки'

    method = models.CharField(
        'Метод',
        max_length=255,
    )
    delivery_kind = models.ForeignKey(
        DeliveryKind,
        on_delete=models.CASCADE,
        related_name='deliveries',
        verbose_name='Разновидность',
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        related_name='deliveries',
        verbose_name='Адрес',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='deliveries',
        verbose_name='Заказчик',
    )

    def __str__(self):
        return f'{self.address} - {self.user}'


# Корзина
class Bucket(TimeBasedModel):
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bucket'
    )
    product = models.ManyToManyField(
        Modification,
        through='BucketModification',
    )

    def __str__(self):
        return f'Корзина - {self.user}'


class BucketModification(models.Model):
    class Meta:
        verbose_name = 'Корзина - Товар'
        verbose_name_plural = 'Корзины - Товары'
        constraints = [
            UniqueConstraint(
                fields=('bucket', 'modification'),
                name='unique_bucket_modification',
            ),
        ]

    bucket = models.ForeignKey(
        Bucket,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Корзина',
    )
    modification = models.ForeignKey(
        Modification,
        on_delete=models.CASCADE,
        related_name='buckets',
        verbose_name='Товар'
    )
    quantity = models.IntegerField(
        'Количество',
        default=0,
    )

    def __str__(self):
        return f'{self.bucket} - {self.modification} {self.quantity} шт.'


class Order(TimeBasedModel):
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    bucket = models.ForeignKey(
        Bucket,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Корзина',
    )
    delivery = models.ForeignKey(
        Delivery,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Доставка',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Заказчик',
    )

    def __str__(self):
        return f'{self.bucket} - {self.delivery}'


# Отзыв
class Recall(TimeBasedModel):
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    EMOTIONS = (
        ('POSITIVE', 'Позитивный'),
        ('NEUTRAL', 'Нейтральный'),
        ('NEGATIVE', 'Негативный'),
        ('IDEA', 'Идея'),
    )

    emotion = models.CharField(
        'Эмоция',
        choices=EMOTIONS,
        max_length=20,
    )
    product_quality = models.IntegerField(
        'Качество еды',
        validators=[positive_number, validate_less_ten]
    )
    ordering = models.IntegerField(
        'Оформление заказа',
        validators=[positive_number, validate_less_ten]
    )
    delivery_speed = models.IntegerField(
        'Скорость доставки',
        validators=[positive_number, validate_less_ten]
    )
    order_number = models.IntegerField(
        'Номер заказа',
        validators=[positive_number]
    )
    comment = models.TextField(
        'Комментарий',
        blank=True,
        null=True,
    )
    file = models.FileField(
        'Файл',
        upload_to='recalls/images/',
        blank=True,
        null=True,
    )
