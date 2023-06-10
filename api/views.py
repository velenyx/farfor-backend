from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.settings import api_settings

from .models import Product, User
from .permissions import AnonUserPermission
from .serializers import ProductSerializer, UserPkTokenLogin


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    # serializer_class = UserSerializer


class ObtainAuthToken(APIView):
    permission_classes = [AnonUserPermission]

    def post(self, request):
        pk = request.data.get('pk')
        if pk:
            user = get_object_or_404(User, pk=pk)
        else:
            user = User()
            # user.save()
        # jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        # jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        # payload = jwt_payload_handler(user)
        # token = jwt_encode_handler(payload)
        return Response({'auth_token': 'yes'})
