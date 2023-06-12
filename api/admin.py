from django.contrib import admin

from .models import (
    Product, Collection, Size, Property, Promotion, Country, City,
)


class ProductPropertyInline(admin.TabularInline):
    model = Product.property.through


class ProductKindInline(admin.TabularInline):
    model = Product.size.through


class CollectionProductInline(admin.TabularInline):
    model = Collection.product.through


class CollectionPropertyInline(admin.TabularInline):
    model = Collection.property.through


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'kind', 'name', 'description', 'promotion', 'discount'
    )
    inlines = (ProductPropertyInline, ProductKindInline,)
    search_fields = ('kind', 'name',)
    empty_value_display = '--пусто--'


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'kind', 'name', 'description', 'promotion', 'discount'
    )
    inlines = (CollectionPropertyInline, CollectionProductInline,)
    search_fields = ('kind', 'name',)
    empty_value_display = '--пусто--'


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'hex_color',)


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')


@admin.register(Size)
class KindAdmin(admin.ModelAdmin):
    list_display = ('pk', 'size', 'measurement')


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'country')
