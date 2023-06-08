from rest_framework import serializers

from .models import Product, Property, ProductSize, User, Size


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

    def get_size(self, obj):
        return f'{obj.size.size}{obj.size.measurement}'


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
            'property',
            'sizes',
        )

    kpfc = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    property = PropertySerializer(many=True, read_only=True)
    sizes = SizeProductSerializer(many=True, read_only=True)

    def get_kpfc(self, obj):
        return {
            'calorie': obj.calorie,
            'proteins': obj.proteins,
            'fats': obj.fats,
            'carbohydrates': obj.carbohydrates
        }

    def get_image(self, obj):
        return '/media/' + obj.image.name


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'email',
        )