from django.urls import path
from .views import *

urlpatterns = [
    path('api_order_create/', Order_api_views.as_view(), name='api_order_create')
]
