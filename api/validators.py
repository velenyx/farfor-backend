from django.core import validators
from django.core.exceptions import ValidationError


positive_number = validators.RegexValidator(
    regex='^[0-9.]+$',
    message='Число должно быть положительным',
)

validate_hex_color = validators.RegexValidator(
    regex='^#[a-zA-Z0-9]+$',
    message='Неправильный формат цвета',
)


def validate_less_hundred(value):
    if value > 100:
        raise ValidationError(
            "%(value)s is not less hundred",
            params={"value": value},
        )


def validate_less_ten(value):
    if value > 10:
        raise ValidationError(
            "%(value)s is not less than ten",
            params={"value": value},
        )
