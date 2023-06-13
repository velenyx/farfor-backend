from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, \
    TokenRefreshView

from .views import ProductViewSet, ObtainAuthToken, UserViewSet

router = DefaultRouter()

router.register('users', UserViewSet)
router.register('products', ProductViewSet)

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
