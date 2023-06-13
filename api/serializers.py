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


class EmailLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {
            'email': {'required': True},
            'password': {'required': True},
        }


class SetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    re_password = serializers.CharField()

    def validate(self, data):
        if data.get('password') != data.get('re_password'):
            raise serializers.ValidationError('Пароли не совпадают')
        return data


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)


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

