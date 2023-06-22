from random import randint
from smtplib import SMTPDataError

from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt import tokens

from .models import Product, User, Country, Promotion, Category
from .serializers import (
    ProductSerializer,
    LocationSerializer,
    EmailSerializer,
    UserSerializer,
    SetPasswordSerializer,
    CodeSerializer,
    EmailLoginSerializer,
    PromotionSerializer,
    CategorySerializer,
    UserMeSerializer, ShortCategorySerializer,
)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'list':
            return ShortCategorySerializer
        return CategorySerializer


class PromotionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    lookup_field = 'slug'


class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    serializer_class = LocationSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'set_password':
            return SetPasswordSerializer
        elif self.action == 'send_code':
            return EmailSerializer
        elif self.action == 'check_code':
            return CodeSerializer
        elif self.action == 'login':
            return EmailLoginSerializer
        elif self.action == 'me':
            return UserMeSerializer
        return UserSerializer

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=[permissions.AllowAny])
    def me(self, request):
        """
        users_me\n
        Возвращает информацию о пользователе, если аноним,
        создается новый пользователь и токен.\n
        Возвращает просто статус кода 200.\n
        """

        user = request.user

        if user.is_anonymous:
            user = User()
            user.save()

        serializer = self.get_serializer(user, context={'user': user})

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['POST'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
        url_path='set-password')
    def set_password(self, request):
        """
        users_set_password\n
        Меняет пароль пользователя\n
        Получает password и re_password.\n
        Возвращает просто статус кода 201, если пароли проходят валидацию.\n
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.set_password(serializer.validated_data.get('password'))
        user.save()
        return Response(status=status.HTTP_201_CREATED)

    @action(
        methods=['POST'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
        url_path='send-code',
    )
    def send_code(self, request):
        """
        users_send_code\n
        Отправка кода.\n
        Получает email, куда нужно будет отправить код, и сам code.\n
        Возвращает просто статус кода 201.\n
        """

        serializer = self.get_serializer(data=request.data)
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
            to=[email]
        )
        msg.attach_alternative(html_body, 'text/html')

        try:
            msg.send()
        except SMTPDataError:
            return Response(status=status.HTTP_429_TOO_MANY_REQUESTS)

        return Response(status=status.HTTP_201_CREATED)

    @action(
        methods=['POST'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
        url_path='check-code',
    )
    def check_code(self, request):
        """
        users_check_code\n
        Проверка кода.\n
        Проверяет код, который передал пользователь, с настоящим кодом.\n
        Если код совпадает, то меняем статус текущего пользователя
        на верифицированного и возвращается его токен,
        либо если уже существует пользователь,
        просто получаем его, и отдаем его токен.\n
        Получает password и re_password.\n
        Возвращает просто статус кода 201, если пароли проходят валидацию.\n
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data.get('code')

        if request.user.code != code:
            return Response(
                {'message': 'Код не совпадает с отправленным на почту'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.filter(
            email=request.user.email, is_verified=True
        ).first()
        if not user:
            user = request.user

        user.is_verified = True
        user.save()

        refresh = tokens.RefreshToken.for_user(user)
        content = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

        return Response(content, status=status.HTTP_201_CREATED)

    @action(
        methods=['POST'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
    )
    def login(self, request):
        """
        users_login\n
        Авторизация через пароль.\n
        Авторизируем пользователя через пароль, если пароль уже задан.\n
        Если пароль не совпадает вернет ошибку 400.\n
        Получает email и password.\n
        Возвращает токены и статус кода 201, если проходит валидацию.\n
        """

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
        return Response(content, status=status.HTTP_201_CREATED)
