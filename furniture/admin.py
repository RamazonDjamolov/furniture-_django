from django.contrib import admin
from .models import *


class orderAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'email', 'adress')
    search_fields = ('full_name', 'email', 'adress')


admin.site.register(Order, orderAdmin)

admin.site.register(OrderItem)
admin.site.register(img)

admin.site.register(Category)

admin.site.register(Product)

admin.site.register(Xonalar)

admin.site.register(Complect_product)
