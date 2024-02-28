from django import forms
from django import forms
from phonenumbers import NumberParseException, parse as parse_phone_number

from .models import *
from .models import validate_phone_number


#
class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

        widgets = {
            'full_name': forms.TextInput(attrs=
                                         {'class': 'full_name_input', 'placeholder': 'full name'}),

            'phone_number': forms.TextInput(attrs=
                                            {'class': 'phone_number_input', 'placeholder': '+9989x xxx xx xx'}),

            'email': forms.EmailInput(
                attrs={'class': 'email_input', 'placeholder': 'exam@example.com'}),

            'adress': forms.TextInput(
                attrs={'class': 'full_name_input', 'placeholder': 'Tshkent city , biromod, home 28 '}),

        }

