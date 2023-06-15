from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import UniqueConstraint

from users_app.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('pk',)
        constraints = [
            UniqueConstraint(
                fields=('username', 'email'),
                name='unique_user',
            ),
        ]

    username = models.CharField(
        'username',
        max_length=255,
        unique=True,
        null=True,
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=255,
        # unique=True,
        null=True,
    )
    full_name = models.CharField(
        'Полное имя',
        max_length=255,
        null=True,
    )
    birthday = models.DateField(
        'Дата рождения',
        null=True,
    )
    sex = models.CharField(
        'Пол',
        choices=(('Мужской', 'M'), ('Женский', 'W')),
        max_length=7,
        null=True,
    )
    code = models.CharField(
        'Код',
        max_length=20,
        null=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        if self.email:
            return self.email
        return str(self.pk)

    @property
    def is_staff(self):
        return self.is_admin
