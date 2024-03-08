from django.urls import path
from .views import *

urlpatterns = [
    path('', main, name='main'),
    path('category/', category_view, name='category'),
    path('toplamlar/', toplam_view, name='toplam'),
    path('toplamlar/<int:id>/', toplam_pr_view, name='toplam_view_pr'),
    path('category/<int:id>/', product_category, name='product_category'),
    path('view_product/<int:id>/', view_product, name='view_product'),
    path('cart/', cart_view, name='cart'),
    path('add/<int:id>/', add_to_cart, name='add')

]