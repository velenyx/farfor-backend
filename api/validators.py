from django.core import validators
from django.core.exceptions import ValidationError


positive_number = validators.RegexValidator(
    regex='^[0-9]+$',
    message='Число должно быть положительным',
)

validate_hex_color = validators.RegexValidator(
    regex='^#[a-zA-Z0-9]+$',
    message='Неправильный формат цвета',
)


def validate_less_hundred(value):
    if value > 100:
        raise ValidationError(
            "%(value)s is not an even number",
            params={"value": value},
        )
