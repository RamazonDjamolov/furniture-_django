from django.shortcuts import render, redirect
from .forms import CheckoutForm
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse


def main(request):
    return render(request, 'main.html')


def cart_view(request):
    forms = CheckoutForm()
    if request.method == 'POST':
        forms = CheckoutForm(request.POST)
        print(forms.is_valid())
        if forms.is_valid():
            email = forms.cleaned_data['email']
            message = "vash zakazniy nomer 101010"

            send_mail(
                'Company Ziyo Nur',
                message,
                'settings.EMAIL_HOST_USER',
                [email],
                fail_silently=False

            )
            forms.save()
            return redirect('cart')

    return render(request, 'cart.html', context={'forms': forms})

    #
    # if request.method == 'POST':
    #     name = request.POST['name']


def category_view(request):
    return render(request, 'category.html')

#
# def cart_view_view(request):
#     return render(request, 'cart.html')
