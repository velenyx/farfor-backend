from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt import tokens
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Product, User
from .permissions import AnonUserPermission
from .serializers import ProductSerializer, UserPkTokenLogin, \
    EmailUserSerializer


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    # serializer_class = UserSerializer


class AuthenticateUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EmailUserSerializer

    def post(self, request):

        return Response({'auth': 'login'})



class ObtainAuthToken(APIView):
    permission_classes = [AnonUserPermission]

    def post(self, request):
        pk = request.data.get('pk')
        if pk:
            user = get_object_or_404(User, pk=pk)
        else:
            user = User()
        refresh = tokens.RefreshToken.for_user(user)
        content = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return Response(content)
