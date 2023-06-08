from django.core import validators
from django.core.exceptions import ValidationError


positive_number = validators.RegexValidator(
    regex='^[0-9]+$',
    message='Число должно быть положительным',
)


def validate_less_hundred(value):
    if value > 100:
        raise ValidationError(
            "%(value)s is not an even number",
            params={"value": value},
        )
