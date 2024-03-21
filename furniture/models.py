from datetime import timezone

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import phonenumbers
from django_ckeditor_5.fields import CKEditor5Field


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

    def __str__(self):
        return self.name


class img(models.Model):
    img = models.ImageField(upload_to='furniture')

    def __str__(self):
        return self.img.url


class Product(models.Model):
    name = models.CharField(max_length=300)
    description = CKEditor5Field('Text', config_name='extends')
    height = models.PositiveIntegerField(default=0)
    length = models.PositiveIntegerField(default=0)
    width = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=30, decimal_places=3, verbose_name='price')
    sale_price = models.DecimalField(max_digits=30, decimal_places=3, verbose_name='sale_price', null=True, blank=True)
    real_price = models.DecimalField(max_digits=30, decimal_places=3, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='category')
    img = models.ManyToManyField(img, related_name='product_img')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + ' ' + str(self.price)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        db_table = 'Product'


class Xonalar(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Xona'
        verbose_name_plural = 'Xonalar'
        db_table = 'Xonalar'


class Complect_product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=30, decimal_places=3)
    sale_price = models.DecimalField(max_digits=30, decimal_places=3)
    real_price = models.DecimalField(max_digits=30, decimal_places=3)
    product = models.ManyToManyField(Product, related_name='complect_product')
    created_at = models.DateTimeField(auto_now_add=True)
    xonalar = models.ForeignKey(Xonalar, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Complect_product'
        verbose_name_plural = 'Complect_products'
        db_table = 'Complect_product'


class Order(models.Model):
    full_name = models.CharField(max_length=100, validators=[full_name])
    phone_number = models.CharField(max_length=13, validators=[validate_phone_number])
    email = models.EmailField()
    adress = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        db_table = 'Order'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    comlect = models.ForeignKey(Complect_product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.order.full_name + " : product -->>"

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
        db_table = 'Order_Item'
