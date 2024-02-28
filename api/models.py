from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import phonenumbers


def validate_phone_number(value):
    num = phonenumbers.parse(str(value))
    if not phonenumbers.is_valid_number(num):
        raise ValidationError('The phone number is not correct ! Please try again.')


def full_name(value):
    x = value.split(" ")
    if len(x) < 2:
        raise ValidationError(_('Toliq ism familiyakamida 3ta sozdan iborat bolishi kereag.'), code='invalid_full_name')


def address(value):
    x = value.split(" ")
    if len(x) < 3:
        raise ValidationError(_('Toliq ism familiyakamida 3ta sozdan iborat bolishi kereag.'), code='invalid_full_name')


class Order(models.Model):
    full_name = models.CharField(max_length=100, validators=[full_name])
    phone_number = models.CharField(max_length=13, validators=[validate_phone_number])
    email = models.EmailField()
    adress = models.CharField(max_length=100)
