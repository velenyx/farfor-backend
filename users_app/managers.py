from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email=None, username=None, password=None, **kwargs):
        if not email and not username:
            raise ValueError('Поле Email должно быть установлено.')

        if email:
            email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            **kwargs
        )

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_user(self, username=None, email=None, password=None, **kwargs):
        kwargs.setdefault('is_superuser', False)
        return self._create_user(
            username=username, email=email, password=password, **kwargs
        )

    def create_superuser(self, username, password, **kwargs):
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_admin', True)
        kwargs.setdefault('is_verified', True)
        user = self.create_user(
            username,
            email=f'{username}@admin.com',
            password=password,
            **kwargs
        )
        user.save(using=self._db)
        return user
