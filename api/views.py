from random import randint
from smtplib import SMTPDataError

from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt import tokens

from .models import Product, User, Collection, Country
from .permissions import AnonUserPermission
from .serializers import (
    ProductSerializer,
    CollectionSerializer,
    LocationSerializer,
    EmailSerializer,
    UserSerializer,
    SetPasswordSerializer,
    CodeSerializer,
    EmailLoginSerializer,
)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # def get_queryset(self):
    #     return Product.objects.filter(is_full=True)


class CollectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer


class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    serializer_class = LocationSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(
        methods=['POST'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
        url_path='set-password')
    def set_password(self, request):
        serializer = SetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.set_password(serializer.validated_data.get('password'))
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['POST'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
        url_path='send-code',
    )
    def send_code(self, request):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        code = ''.join([str(randint(0, 9)) for _ in range(5)])

        if not email:
            return Response({'message': 'Поле email обязательное!'},
                            status=status.HTTP_400_BAD_REQUEST)

        request.user.email = email
        request.user.code = code
        request.user.save()

        html_body = render_to_string(
            'email_templates/confirm_verification_email.html',
            {'code': code},
        )
        msg = EmailMultiAlternatives(
            subject=f'Код подтверждения - {code}',
            to=['jotaro.kyoujo@yandex.ru']
        )
        msg.attach_alternative(html_body, 'text/html')

        try:
            msg.send()
        except SMTPDataError:
            return Response(status=status.HTTP_429_TOO_MANY_REQUESTS)

        return Response(status=status.HTTP_200_OK)

    @action(
        methods=['POST'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
        url_path='check-code',
    )
    def check_code(self, request):
        serializer = CodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data.get('code')

        if request.user.code != code:
            return Response(
                {'message': 'Код не совпадает с отправленным на почту'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.filter(email=request.user.email, is_verified=True)
        if not user:
            user = request.user

        user.is_verified = True
        user.save()

        refresh = tokens.RefreshToken.for_user(user)
        content = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

        return Response(content, status=status.HTTP_200_OK)

    @action(
        methods=['POST'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
    )
    def login(self, request):
        serializer = EmailLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(
            User,
            email=serializer.validated_data.get('email'),
            is_verified=True
        )

        check_password = user.check_password(
            serializer.validated_data.get('password'))
        if not check_password:
            return Response(
                data={'message': 'Пароль не совпадает'},
                status=status.HTTP_400_BAD_REQUEST)

        refresh = tokens.RefreshToken.for_user(user)
        content = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return Response(content, status=status.HTTP_200_OK)


class ObtainAuthToken(APIView):
    """
    Отдает Token.
    Если передали email получает пользователя и создает для него Token.
    Если не передали создается новый пользователь и создается Token.
    """
    permission_classes = [AnonUserPermission]
    serializer_class = EmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data:
            user = get_object_or_404(
                User, email=serializer.validated_data.get('email')
            )
        else:
            user = User()
            user.save()

        refresh = tokens.RefreshToken.for_user(user)
        content = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return Response(content)
