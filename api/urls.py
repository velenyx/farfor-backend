from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from .views import (
    ProductViewSet,
    CollectionViewSet,
    LocationViewSet,
    ObtainAuthToken,
    UserViewSet, PromotionViewSet, CategoryViewSet
)

router = DefaultRouter()

router.register('users', UserViewSet)
router.register('products', ProductViewSet)
router.register('collections', CollectionViewSet)
router.register('categories', CategoryViewSet)
router.register('promotions', PromotionViewSet)
router.register('locations', LocationViewSet)

app_name = 'app'
urlpatterns = [
    # path('send_code', )
    path('auth/token/', ObtainAuthToken.as_view(), name='get_token'),
    # path('token/', TokenObtainPairView.as_view(),
    #      name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(),
    #      name='token_refresh'),
    path('', include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
