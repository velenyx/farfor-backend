from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, \
    TokenRefreshView

from .views import ProductViewSet, ObtainAuthToken

router = DefaultRouter()

router.register('products', ProductViewSet)

app_name = 'app'
urlpatterns = [
    path('auth/token/login/', ObtainAuthToken.as_view(), name='get_token'),
    # path('token/', TokenObtainPairView.as_view(),
    #      name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(),
    #      name='token_refresh'),
    path('', include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
