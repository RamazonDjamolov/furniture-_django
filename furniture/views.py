from django.shortcuts import render, redirect
from .forms import CheckoutForm
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from .models import *


def func_category(request):
    categories = Category.objects.all()
    return categories


def main(request):
    category = func_category(request)
    return render(request, 'main.html', {'category': category})


# categoriyaga tegishli bolgan hamma narsalarni boshlanishi


def product_category(request, id: int):
    products = Product.objects.all().filter(category_id=id).all()

    category = func_category(request)

    return render(request, 'category.html', context={
        'products': products,
        'category': category
    })


def cart_view(request):
    category = func_category(request)

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

    return render(request, 'cart.html', context={
        'forms': forms,
        'category': category

    })

    #
    # if request.method == 'POST':
    #     name = request.POST['name']


def category_view(request):
    category = func_category(request)
    products = Product.objects.all()

    return render(request, 'category.html', {
        'category': category,
        'products': products

    })


def view_product(request, id: int):
    category = func_category(request)
    product = Product.objects.get(id=id)

    return render(request, 'view_product.html', context={
        'category': category,
        'products': product
    })
#
# def cart_view_view(request):
#     return render(request, 'cart.html')
