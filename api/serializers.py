from rest_framework import serializers
from api.models import *




class orderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
