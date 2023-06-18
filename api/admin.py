from django.contrib import admin

from .models import (
    Product,
    Size,
    Property,
    Promotion,
    Country,
    City,
    Condition,
    Category,
    Banner,
)


class PromotionConditionInline(admin.TabularInline):
    model = Promotion.condition.through


class ProductPropertyInline(admin.TabularInline):
    model = Product.property.through


class ProductSizeInline(admin.TabularInline):
    model = Product.size.through


class ProductCategoryInline(admin.TabularInline):
    model = Product.category.through


class ProductCollectionInline(admin.TabularInline):
    model = Product.collection.through
    fk_name = 'parent_product'


class CategoryBannerInline(admin.TabularInline):
    model = Category.banner.through


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'description', 'promotion', 'discount'
    )
    inlines = (
        ProductPropertyInline,
        ProductSizeInline,
        ProductCategoryInline,
        ProductCollectionInline,
    )
    search_fields = ('category', 'name',)
    empty_value_display = '--пусто--'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug',)
    prepopulated_fields = {"slug": ("name",)}
    inlines = (CategoryBannerInline,)


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'title', 'slug',)
    inlines = (PromotionConditionInline,)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slug')
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'size', 'measurement')


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'country')


@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
