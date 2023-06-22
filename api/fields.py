from django import forms
from django.db import models
from django.core import exceptions
from django.utils.translation import gettext_lazy as _


class CustomFloatField(models.Field):
    empty_strings_allowed = False
    default_error_messages = {
        "invalid": _("“%(value)s” value must be a float or number."),
    }
    description = _("Floating point number and Integer number")

    def __init__(self, *args, **kwargs):
        self.is_float = False
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if value is None:
            return None
        try:
            if not float(value).is_integer():
                self.is_float = True
                return float(value)
            return int(value)
        except (TypeError, ValueError) as e:
            raise e.__class__(
                "Field '%s' expected a number but got %r." % (
                self.name, value),
            ) from e

    def get_internal_type(self):
        if self.is_float:
            return "FloatField"
        return "IntegerField"

    def to_python(self, value):
        if value is None:
            return value
        try:
            if not float(value).is_integer():
                self.is_float = True
                return float(value)
            return int(value)
        except (TypeError, ValueError):
            raise exceptions.ValidationError(
                self.error_messages["invalid"],
                code="invalid",
                params={"value": value},
            )

    def formfield(self, **kwargs):
        return super().formfield(
            **{
                "form_class": forms.CharField,
                **kwargs,
            }
        )
