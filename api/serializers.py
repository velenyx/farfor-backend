from rest_framework import serializers

from .models import Product, Property, ProductSize, User, Size, Promotion, \
    Collection, CollectionProduct


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
        fields = ('pk', 'size', 'price', 'weight')

    pk = serializers.PrimaryKeyRelatedField(
        queryset=Size.objects.all(),
        source='size.id'
    )
    size = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    weight = serializers.SerializerMethodField()

    def get_size(self, obj):
        return f'{obj.size.size}{obj.size.measurement}'

    def get_price(self, obj):
        return f'{obj.price}₽'

    def get_weight(self, obj):
        return {obj.weight}


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ('pk', 'name', 'hex_color')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'pk',
            'kind',
            'name',
            'description',
            'promotion',
            'discount',
            'kpfc',
            'image',
            'properties',
            'sizes',
        )

    kpfc = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    promotion = PromotionSerializer(read_only=True)
    properties = PropertySerializer(
        many=True, read_only=True, source='property'
    )
    sizes = SizeProductSerializer(many=True, read_only=True)

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


class ShortProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionProduct
        fields = ('pk', 'name', 'description', 'image')

    name = serializers.SerializerMethodField(source='product.name')
    description = serializers.CharField(source='product.description')
    image = serializers.SerializerMethodField()

    def get_name(self, obj):
        if obj.is_full:
            return obj.product.name
        elif obj.product.sizes.last().size.measurement == 'шт':
            if len(obj.product.sizes.all()) > 1:
                return f'{obj.product.name} 1/2'
            return obj.product.name
        return f'{obj.product.name}см'

    def get_image(self, obj):
        if obj.product.image.name:
            return '/media/' + obj.product.image.name


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = (
            'pk',
            'kind',
            'name',
            'description',
            'price',
            'weight',
            'amount',
            'promotion',
            'discount',
            'kpfc',
            'image',
            'properties',
            'products',
        )

    price = serializers.SerializerMethodField()
    weight = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()
    kpfc = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    promotion = PromotionSerializer(read_only=True)
    properties = PropertySerializer(many=True, read_only=True, source='property')
    products = ShortProductSerializer(many=True, read_only=True)

    def get_price(self, obj):
        return f'{obj.price}₽'

    def get_weight(self, obj):
        total_weight = 0
        for collection in obj.products.all():
            max_size = 0
            for size in collection.product.sizes.all():
                max_size = size.weight if size.weight > max_size else max_size

            total_weight += max_size

        return total_weight

    def get_amount(self, obj):
        amount = 0
        for collection in obj.products.all():
            if collection.product.sizes.last().size.measurement == 'см':
                return None
            sorted_sizes = sorted(
                map(lambda x: x.size.size, collection.product.sizes.all())
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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'email',
        )
