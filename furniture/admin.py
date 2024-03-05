from django.contrib import admin
from .models import Order, OrderItem, Product, img, Category

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(img)
