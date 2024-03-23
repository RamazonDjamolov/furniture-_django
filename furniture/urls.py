from django.urls import path
from .views import *

urlpatterns = [
    path('', main, name='main'),
    path('category/', category_view, name='category'),
    path('toplamlar/<str:name>/', toplam_view, name='toplam'),
    path('toplamlar_view_pr/<int:id>/', toplam_pr_view, name='toplam_view_pr'),
    path('category/<str:name>/', product_category, name='product_category'),
    path('view_product/<int:id>/', view_product, name='view_product'),
    path('cart/', cart_view, name='cart'),
    path('add_to_cart/<int:id>/', add_to_cart, name='add'),
    path('add_to_cart2/<int:id>/', add_to_cart2, name='add2'),
    path('add_toplam/<int:id>/', add_to_cart_toplam, name='add_to_cart_toplam'),
    path('add_toplam2/<int:id>/', add_to_cart_toplam2, name='add_to_cart_toplam2'),
    path('add/<str:id>/', add, name='ad'),
    path('delete/<int:id>/', delete, name='delete'),
    path('add_top/<str:id>/', add_top, name='add_top'),
    path('sub/<str:id>/', sub, name='sub'),
    path('sub_top/<str:id>/', sub_top, name='sub_top'),
    path('delete_top/<str:id>/', delete_top, name='delete_top'),
    path('search/', search, name='search'),
    path('new_product', new_product, name='new_product'),
    # path('products_main/<str:name>/', products_main, name="products_main")
    # path('404', handler404, )

]
