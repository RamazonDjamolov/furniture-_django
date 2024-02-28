from django.contrib import admin
from .models import Order, OrderItem, Poduct, img, Category

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Poduct)
admin.site.register(Category)
admin.site.register(img)
