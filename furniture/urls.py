from django.urls import path
from .views import *

urlpatterns = [
    path('', main, name='main'),
    path('category/', category_view, name='category'),
    path('category/<int:id>/', product_category, name='product_category'),
    path('view_product/<int:id>/', view_product, name='view_product'),
    path('cart/', cart_view, name='cart')

]
