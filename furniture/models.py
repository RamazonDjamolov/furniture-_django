from datetime import timezone

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import phonenumbers


def validate_phone_number(value):
    if value.startswith('+'):
        num = phonenumbers.parse(str(value), region="UZ")
        if not phonenumbers.is_valid_number(num):
            raise ValidationError(
                f' The length of your number should be 13, but the length of your number is {len(value)}')
    else:

        raise ValidationError(
            f' put your number + at the beginning')


def full_name(value):
    x = value.split(" ")
    if len(x) < 2:
        raise ValidationError(_('Toliq ism familiyakamida 3ta sozdan iborat bolishi kereag.'), code='invalid_full_name')


def address(value):
    x = value.split(" ")
    if len(x) < 3:
        raise ValidationError(_('Toliq ism familiyakamida 3ta sozdan iborat bolishi kereag.'), code='invalid_full_name')


class Category(models.Model):
    name = models.CharField(max_length=200)


class img(models.Model):
    img = models.ImageField(upload_to='furniture')


class Poduct(models.Model):
    name = models.CharField(max_length=300)
    img = models.ManyToManyField(img)
    description = models.TextField()
    height = models.DecimalField(max_digits=5, decimal_places=2)
    length = models.DecimalField(max_digits=5, decimal_places=2)
    width = models.DecimalField(max_digits=5, decimal_places=2)
    price = models.DecimalField(max_digits=1000, decimal_places=10)
    sale_price = models.DecimalField(max_digits=3, decimal_places=1)
    real_price = models.DecimalField(max_digits=1000, decimal_places=10)
    created_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    full_name = models.CharField(max_length=100, validators=[full_name])
    phone_number = models.CharField(max_length=13, validators=[validate_phone_number])
    email = models.EmailField()
    adress = models.CharField(max_length=100)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Poduct, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField()
