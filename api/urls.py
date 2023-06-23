from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from .views import (
    ProductViewSet,
    LocationViewSet,
    UserViewSet,
    PromotionViewSet,
    CategoryViewSet,
    DeliveryViewSet, AddressViewSet, BucketViewSet,
)

router = DefaultRouter()

router.register('users', UserViewSet)
router.register('products', ProductViewSet)
router.register('categories', CategoryViewSet)
router.register('buckets', BucketViewSet)
router.register('addresses', AddressViewSet)
router.register('deliveries', DeliveryViewSet)
router.register('promotions', PromotionViewSet)
router.register('locations', LocationViewSet)

app_name = 'app'
urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
