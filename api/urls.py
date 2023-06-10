from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from .views import ProductViewSet, CollectionViewSet

router = DefaultRouter()

router.register('products', ProductViewSet)
router.register('collections', CollectionViewSet)

app_name = 'app'
urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
