from django.urls import path
from .views import *

urlpatterns = [
    path('', main, name='main'),
    path('category/', category_view, name='category'),
    path('toplamlar/<int:id>/', toplam_view, name='toplam'),
    path('toplamlar/<int:id>/', toplam_pr_view, name='toplam_view_pr'),
    path('category/<int:id>/', product_category, name='product_category'),
    path('view_product/<int:id>/', view_product, name='view_product'),
    path('cart/', cart_view, name='cart'),
    path('add_to_cart/<int:id>/', add_to_cart, name='add'),
    path('add_toplam/<int:id>/', add_to_cart_toplam, name='add_to_cart_toplam'),
    path('add/<str:id>/', add, name='ad'),
    path('delete/<int:id>/', delete, name='delete'),
    path('add_top/<str:id>/', add_top, name='add_top'),
    path('sub/<str:id>/', sub, name='sub'),
    path('sub_top/<str:id>/', sub_top, name='sub_top'),
    path('delete_top/<str:id>/', delete_top, name='delete_top'),
    path('search/', search, name='search'),

]
