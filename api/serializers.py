import math

from rest_framework import serializers
from rest_framework_simplejwt import tokens

from .models import (
    Product,
    Property,
    ProductSize,
    User,
    Size,
    Promotion,
    Collection,
    Country,
    City,
    Category,
    Banner,
    ProductCategory,
)

from .utils import get_sizes_type_of_number


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ('pk', 'name', 'icon')

    icon = serializers.SerializerMethodField()

    def get_icon(self, obj):
        return '/media/' + obj.icon.name


class SizeProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = ('pk', 'size', 'price', 'discount_price', 'weight')

    pk = serializers.PrimaryKeyRelatedField(
        queryset=Size.objects.all(),
        source='size.id'
    )
    size = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    discount_price = serializers.SerializerMethodField()
    weight = serializers.SerializerMethodField()

    def get_size(self, obj):
        return f'{obj.size.size}{obj.size.measurement}'

    def get_price(self, obj):
        return f'{obj.price}₽'

    def get_discount_price(self, obj):
        if obj.product.discount:
            return f'{math.ceil(obj.price * (1 - obj.product.discount / 100))}₽'
        return f'{obj.price}₽'

    def get_weight(self, obj):
        return obj.weight


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


class ShortProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('pk', 'name', 'description', 'image')

    pk = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='child_product.id')
    name = serializers.SerializerMethodField(source='child_product.name')
    description = serializers.CharField(source='child_product.description')
    image = serializers.SerializerMethodField()

    def get_name(self, obj):
        if obj.is_full:
            return obj.child_product.name
        elif obj.child_product.sizes.last().size.measurement == 'шт':
            if len(obj.child_product.sizes.all()) > 1:
                return f'{obj.child_product.name} 1/2'
            return obj.child_product.name
        return (f'{obj.child_product.name} '
                f'{obj.child_product.sizes.last().size.size}см')

    def get_image(self, obj):
        if obj.child_product.image.name:
            return '/media/' + obj.child_product.image.name


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
            'properties',
            'sizes',
        )

    total_weight = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()
    kpfc = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    promotion = ShortPromotionSerializer(read_only=True)
    components = ShortProductSerializer(many=True, read_only=True)
    properties = PropertySerializer(
        many=True, read_only=True, source='property')
    sizes = SizeProductSerializer(many=True, read_only=True)

    def get_total_weight(self, obj):
        total_weight = 0

        for collection in obj.components.all():
            weights = [
                size.weight for size in collection.child_product.sizes.all()
            ]
            if collection.is_full:
                total_weight += max(weights)
                continue
            total_weight += min(weights)

        if not total_weight:
            return None
        return total_weight

    def get_amount(self, obj):
        if not obj.components.all():
            return None

        amount = 0

        for collection in obj.components.all():
            if collection.child_product.sizes.last().size.measurement == 'см':
                return None
            sizes = [i.size.size for i in collection.child_product.sizes.all()]
            sorted_sizes = sorted(
                map(lambda x: x, get_sizes_type_of_number(sizes))
            )

            if collection.is_full:
                amount += sorted_sizes[-1]
            else:
                amount += sorted_sizes[0]

        return f'{amount} шт'

    def get_kpfc(self, obj):
        return {
            'calorie': obj.calorie,
            'proteins': obj.proteins,
            'fats': obj.fats,
            'carbohydrates': obj.carbohydrates
        }

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
            'sizes',
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
    kpfc = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    components = ShortProductSerializer(many=True, read_only=True, source='product.components')
    properties = PropertySerializer(
        many=True, read_only=True, source='product.property')
    sizes = SizeProductSerializer(
        many=True, read_only=True, source='product.sizes')

    def get_total_weight(self, obj):
        total_weight = 0

        for collection in obj.product.components.all():
            weights = [
                size.weight for size in collection.child_product.sizes.all()
            ]
            if collection.is_full:
                total_weight += max(weights)
                continue
            total_weight += min(weights)

        if not total_weight:
            return None
        return total_weight

    def get_amount(self, obj):
        if not obj.product.components.all():
            return None

        amount = 0

        for collection in obj.product.components.all():
            if collection.child_product.sizes.last().size.measurement == 'см':
                return None
            sizes = [i.size.size for i in collection.child_product.sizes.all()]
            sorted_sizes = sorted(
                map(lambda x: x, get_sizes_type_of_number(sizes))
            )

            if collection.is_full:
                amount += sorted_sizes[-1]
            else:
                amount += sorted_sizes[0]

        return f'{amount} шт'

    def get_kpfc(self, obj):
        return {
            'calorie': obj.product.calorie,
            'proteins': obj.product.proteins,
            'fats': obj.product.fats,
            'carbohydrates': obj.product.carbohydrates
        }

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
                'Поле code должно быть меньше 5')
        for v in code:
            try:
                int(v)
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
