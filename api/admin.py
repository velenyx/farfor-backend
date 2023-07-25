from django.contrib import admin

from .models import (
    Product,
    Property,
    Promotion,
    Country,
    City,
    Condition,
    Category,
    Banner,
    Bucket,
    Address,
    DeliveryKind,
    Delivery, Order, Modification, KPFC, Recall,
)


class PromotionConditionInline(admin.TabularInline):
    model = Promotion.condition.through


class ProductPropertyInline(admin.TabularInline):
    model = Product.property.through


class ProductModificationInline(admin.TabularInline):
    model = Product.modification.through


class ProductCategoryInline(admin.TabularInline):
    model = Product.category.through


class ProductComponentInline(admin.TabularInline):
    model = Product.component.through


class CategoryBannerInline(admin.TabularInline):
    model = Category.banner.through


class BucketProductInline(admin.TabularInline):
    model = Bucket.product.through


@admin.register(Bucket)
class BucketAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user',)
    inlines = (BucketProductInline,)


@admin.register(DeliveryKind)
class DeliveryCostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'status', 'message', 'price')
    search_fields = ('status',)


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'method')
    search_fields = ('method', 'delivery_kind', 'address', 'user',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'bucket', 'delivery')


@admin.register(Recall)
class RecallAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'emotion',
        'product_quality',
        'ordering',
        'delivery_speed',
        'order_number'
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('pk', 'city', 'street', 'house')
    search_fields = ('city', 'street',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'description', 'promotion'
    )
    inlines = (
        ProductPropertyInline,
        ProductModificationInline,
        ProductCategoryInline,
        ProductComponentInline,
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
    list_display = ('pk', 'name', 'slug')
    prepopulated_fields = {"slug": ("name",)}


@admin.register(KPFC)
class KPFCAdmin(admin.ModelAdmin):
    list_display = ('pk', 'calories', 'proteins', 'fats', 'carbohydrates',)


@admin.register(Modification)
class ModificationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'mode', 'amount', 'price', 'weight',)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'country')


@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
