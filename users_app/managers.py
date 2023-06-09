from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email=None, username=None, password=None, **kwargs):
        if not email and not username:
            raise ValueError('Поле Email должно быть установлено.')

        if email:
            email = self.normalize_email(email)
            if not username:
                username = email
            user = self.model(
                email=email,
                username=username,
                **kwargs
            )

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **kwargs):
        kwargs.setdefault('is_admin', False)
        kwargs.setdefault('is_superuser', False)
        return self._create_user(
            username=username, email=email, password=password, **kwargs
        )

    def create_superuser(self, username, password, **kwargs):
        kwargs.setdefault('is_superuser', True)
        user = self.create_user(
            username,
            email=f'{username}@admin.com',
            password=password,
            **kwargs
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
