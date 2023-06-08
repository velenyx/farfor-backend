from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from .views import ProductViewSet

router = DefaultRouter()

router.register('products', ProductViewSet)

app_name = 'app'
urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
