from django.shortcuts import render
from .serializers import *
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView


class Order_api_views(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = orderSerializer

# Create your views here.
