from django import forms
from .models import *


#
class checkoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

