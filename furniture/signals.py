from venv import create

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import Product, Complect_product




@receiver(pre_save, sender=Product)
def create_user_profile(sender, instance, **kwargs):
    if instance.pk is None:
        price = instance.price
        sale = instance.sale_price
        if sale == None:
            sale = 0
        instance.real_price = price - sale
    else:
        price = instance.price
        sale = instance.sale_price
        if sale == None:
            sale = 0
        instance.real_price = price - sale





# complect product
@receiver(pre_save, sender=Complect_product)
def create_user_profile(sender, instance, **kwargs):
    if instance.pk is None:
        price = instance.price
        sale = instance.sale_price
        if sale == None:
            sale = 0
        instance.real_price = price - sale
    else:
        price = instance.price
        sale = instance.sale_price
        if sale == None:
            sale = 0
        instance.real_price = price - sale
