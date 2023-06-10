from django.contrib import admin

from .models import Product, Size, Property, Promotion


class ProductPropertyInline(admin.TabularInline):
    model = Product.property.through


class ProductKindInline(admin.TabularInline):
    model = Product.size.through


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description', 'promotion', 'discount')
    inlines = (ProductPropertyInline, ProductKindInline,)
    search_fields = ('name',)
    empty_value_display = '--пусто--'


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'hex_color',)


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')


@admin.register(Size)
class Kind(admin.ModelAdmin):
    list_display = ('pk', 'size', 'measurement')
