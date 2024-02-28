from django.urls import path
from .views import *
urlpatterns = [
    path('', main, name='main'),
    path('category/', category_view, name='category'),
    path('cart/', cart_view, name='cart')
]