import math

from rest_framework import serializers
from rest_framework_simplejwt import tokens
from drf_base64.fields import Base64FileField

from .models import (
    Product,
    Property,
    ProductModification,
    User,
    Modification,
    Promotion,
    Component,
    Country,
    City,
    Category,
    Banner,
    ProductCategory,
    Delivery,
    Address,
    DeliveryKind,
    Bucket,
    BucketModification,
    KPFC, Recall,
)


class KPFCSerializer(serializers.ModelSerializer):
    class Meta:
        model = KPFC
        fields = ('calories', 'proteins', 'fats', 'carbohydrates',)


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ('pk', 'name', 'icon')

    icon = serializers.SerializerMethodField()

    def get_icon(self, obj):
        return '/media/' + obj.icon.name


class ProductModificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModification
        fields = (
            'pk',
            'name',
            'mode',
            'amount',
            'weight',
            'total_price',
            'price',
        )

    name = serializers.CharField(source='modification.name')
    mode = serializers.CharField(source='modification.mode')
    amount = serializers.IntegerField(source='modification.amount')
    weight = serializers.IntegerField(source='modification.weight')
    total_price = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        return f'{obj.modification.price}₽'

    def get_price(self, obj):
        try:
            price = obj.modification.price * (1 - obj.product.discount / 100)
            price = math.ceil(price)
            return f'{price}₽'
        except TypeError:
            return f'{obj.modification.price}₽'


class ShortPromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ('pk', 'name', 'hex_color')


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('pk', 'title', 'description', 'image', 'slug')

    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        return '/media/' + obj.image.name


# Promotion
class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ('pk', 'title', 'description', 'slug', 'image', 'conditions')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }

    image = serializers.SerializerMethodField()
    conditions = serializers.SerializerMethodField()

    def get_image(self, obj):
        return '/media/' + obj.image.name

    def get_conditions(self, obj):
        conditions = [value.condition.name for value in obj.conditions.all()]
        if obj.start_date and obj.end_date:
            date_condition = f'Период проведения акции: ' \
                             f'{obj.start_date.strftime("%Y.%m.%d")} — ' \
                             f'{obj.end_date.strftime("%Y.%m.%d")}'
            conditions = [date_condition, *conditions]
        return conditions


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = ('pk', 'name', 'description', 'image')

    pk = serializers.PrimaryKeyRelatedField(
        queryset=Modification.objects.all(), source='modification.id')
    name = serializers.CharField(source='modification.name')
    description = serializers.CharField(source='modification.description')
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        image = obj.modification.products.first().image
        if image:
            return '/media/' + image.name


# Product
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'pk',
            'name',
            'description',
            'promotion',
            'discount',
            'total_weight',
            'amount',
            'kpfc',
            'image',
            'components',
            'modifications',
            'properties',
        )

    total_weight = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()
    kpfc = KPFCSerializer()
    image = serializers.SerializerMethodField()
    promotion = ShortPromotionSerializer(read_only=True)
    components = ComponentSerializer(many=True, read_only=True)
    properties = PropertySerializer(
        many=True, read_only=True, source='property')
    modifications = ProductModificationSerializer(many=True, read_only=True)

    def get_total_weight(self, obj):
        if not obj.components.all():
            return None

        total_weight = 0

        for components in obj.components.all():
            total_weight += components.modification.weight

        return total_weight

    def get_amount(self, obj):
        if not obj.components.all():
            return None

        amount = 0

        for component in obj.components.all():
            amount += component.modification.amount

        return amount

    def get_image(self, obj):
        if obj.image:
            return '/media/' + obj.image.name


# Category
class CategoryProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = (
            'pk',
            'name',
            'description',
            'promotion',
            'discount',
            'total_weight',
            'amount',
            'kpfc',
            'image',
            'components',
            'properties',
            'modifications',
        )

    pk = serializers.PrimaryKeyRelatedField(
        source='product.pk', read_only=True)
    name = serializers.CharField(source='product.name')
    description = serializers.CharField(source='product.description')
    promotion = ShortPromotionSerializer(
        read_only=True, source='product.promotion')
    total_weight = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()
    discount = serializers.IntegerField(source='product.discount')
    kpfc = KPFCSerializer(source='product')
    image = serializers.SerializerMethodField()
    components = ComponentSerializer(
        many=True, read_only=True, source='product.components')
    properties = PropertySerializer(
        many=True, read_only=True, source='product.property')
    modifications = ProductModificationSerializer(
        many=True, read_only=True, source='product.modifications')

    def get_total_weight(self, obj):
        if not obj.product.components.all():
            return None

        total_weight = 0

        for components in obj.product.components.all():
            total_weight += components.modification.weight

        return total_weight

    def get_amount(self, obj):
        if not obj.product.components.all():
            return None

        amount = 0

        for component in obj.product.components.all():
            amount += component.modification.amount

        return amount

    def get_image(self, obj):
        if obj.product.image:
            return '/media/' + obj.product.image.name


class ShortCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('pk', 'name', 'slug', 'image')

    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        return '/media/' + obj.image.name


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = (
            'pk',
            'name',
            'description',
            'slug',
            'image',
            'banners',
            'products',
            'tags',
        )
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }

    image = serializers.SerializerMethodField()
    banners = BannerSerializer(many=True, read_only=True, source='banner')
    products = CategoryProductsSerializer(
        many=True, read_only=True)
    tags = serializers.SerializerMethodField()

    def get_image(self, obj):
        return '/media/' + obj.image.name

    def get_tags(self, obj):
        result = []
        for product in obj.products.all():
            for tag in product.product.properties.all():
                result.append(
                    {
                        'pk': tag.property.pk,
                        'name': tag.property.name,
                        'slug': tag.property.slug,
                    }
                )
        return result


# Адрес
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            'pk',
            'city',
            'street',
            'house',
            'apartment',
            'porch',
            'floor',
            'intercom',
            'notes',
            'user'
        )

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())


# Для Delivery
class DeliveryKindSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryKind
        fields = ('price', 'message', 'status')


class DeliveryPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = (
            'pk',
            'method',
            'delivery_kind',
            'address_id',
            'user',
        )

    delivery_kind = serializers.CharField(source='delivery_kind.status')
    address_id = serializers.PrimaryKeyRelatedField(
        source='address', queryset=Address.objects.all())
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        delivery_status = validated_data.get('delivery_kind')

        delivery_kind, _ = DeliveryKind.objects.get_or_create(
            status=delivery_status.get('status'))

        delivery = Delivery.objects.create(
            method=validated_data.get('method'),
            address=validated_data.get('address'),
            delivery_kind=delivery_kind,
            user=validated_data.get('user'),
        )

        return delivery

    def update(self, instance, validated_data):
        try:
            delivery_status = validated_data.pop('delivery_kind')

            delivery_kind, _ = DeliveryKind.objects.get_or_create(
                status=delivery_status.get('status'))

            instance.delivery_kind = delivery_kind
        except Exception as _:
            pass

        super().update(instance, validated_data)
        return instance


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = (
            'pk',
            'method',
            'cost',
            'address_id',
        )

    cost = DeliveryKindSerializer(source='delivery_kind')
    address_id = serializers.PrimaryKeyRelatedField(
        source='address', queryset=Address.objects.all())


# Для Bucket
class BucketProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = BucketModification
        fields = (
            'pk',
            'name',
            'description',
            'price',
            'total_price',
            'weight',
            'image',
            'quantity',
        )

    pk = serializers.PrimaryKeyRelatedField(
        queryset=Modification.objects.all())
    name = serializers.CharField(source='modification.name')
    description = serializers.CharField(source='modification.description')
    price = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    weight = serializers.IntegerField(source='modification.weight')
    image = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        return f'{obj.modification.price}₽'

    def get_price(self, obj):
        try:
            price = obj.modification.price * (1 - obj.modification.products.first().discount / 100)
            price = math.ceil(price)
            return f'{price}₽'
        except TypeError:
            return f'{obj.modification.price}₽'

    def get_image(self, obj):
        return '/media/' + obj.modification.products.first().image.name


class BucketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bucket
        fields = ('pk', 'products', 'products_count', 'price')

    products = BucketProductSerializer(many=True)
    products_count = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    def get_products_count(self, obj):
        if not obj.products.all():
            return None
        return len(obj.products.all())

    def get_price(self, obj):
        if not obj.products.all():
            return None

        price = 0

        for product in obj.products.all():
            modification = product.modification

            discount = 1 - (modification.products.first().discount / 100)
            discount_price = math.ceil(modification.price * discount)

            price += discount_price * product.quantity

        return f"{price}₽"


# Для Recalls
class RecallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recall
        fields = (
            'pk',
            'emotion',
            'product_quality',
            'ordering',
            'delivery_speed',
            'order_number',
            'comment',
            'file',
        )

    file = serializers.SerializerMethodField()

    def get_file(self, obj):
        return '/media/' + obj.file.name if obj.file else None


class RecallPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recall
        fields = (
            'pk',
            'emotion',
            'product_quality',
            'ordering',
            'delivery_speed',
            'order_number',
            'comment',
            'file',
        )

    file = Base64FileField(required=False, write_only=True)


# Для Users
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'client_id',
            'email',
            'full_name',
            'birthday',
            'sex',
            'code',
            'is_verified',
        )

    client_id = serializers.PrimaryKeyRelatedField(
        source='pk', queryset=User.objects.all())


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'client_id',
            'email',
            'full_name',
            'birthday',
            'sex',
            'code',
            'is_verified',
        )

    client_id = serializers.PrimaryKeyRelatedField(
        source='pk', queryset=User.objects.all())

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user = self.context['user']

        refresh = tokens.RefreshToken.for_user(user)

        data['access'] = str(refresh.access_token)
        data['refresh'] = str(refresh)
        return data


class EmailLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {
            'email': {'required': True},
            'password': {'required': True},
        }


class SetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    re_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data.get('password') != data.get('re_password'):
            raise serializers.ValidationError('Пароли не совпадают')
        return data


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, write_only=True)


class CodeSerializer(serializers.Serializer):
    code = serializers.CharField()

    def validate(self, data):
        code = data.get('code')
        if len(code) > 5:
            raise serializers.ValidationError(
                'В поле code элементов должно быть равно 5')

        try:
            int(code)
        except Exception:
            raise serializers.ValidationError(
                'Поле code должна состоять из цифр'
            )

        return data


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('pk', 'name')


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('pk', 'country', 'cities')

    country = serializers.CharField(source='name')
    cities = serializers.SerializerMethodField()

    def get_cities(self, obj):
        return [city.name for city in obj.cities.all()]
