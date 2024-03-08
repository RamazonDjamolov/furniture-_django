from django.shortcuts import render, redirect
from .forms import CheckoutForm
from django.core.mail import send_mail
from django.utils.datastructures import MultiValueDictKeyError

from django.conf import settings
from django.http import HttpResponse
from .models import *


def func_category(request):
    categories = Category.objects.all()
    return categories


def get_total_item(request):
    cart = request.session.get('cart', {})
    return sum(cart.values())


def main(request):
    category = func_category(request)
    total_item = get_total_item(request)
    return render(request, 'main.html', {
        'category': category,
        'total_item': total_item
    })


# categoriyaga tegishli bolgan hamma narsalarni boshlanishi


def product_category(request, id: int):
    products = Product.objects.all().filter(category_id=id).all()
    category = func_category(request)
    total_item = get_total_item(request)

    return render(request, 'category.html', context={
        'products': products,
        'category': category,
        'total_item': total_item
    })


def category_view(request):
    category = func_category(request)
    products = Product.objects.all()
    total_item = get_total_item(request)

    return render(request, 'category.html', {
        'category': category,
        'products': products,
        'total_item': total_item

    })


# toplarga

def toplam_view(request):
    total_item = get_total_item(request)
    obj = Complect_product.objects.all()
    category = func_category(request)
    return render(request, template_name='toplamlar.html', context={
        'total_item': total_item,
        'products': obj,
        'category': category
    })


def toplam_pr_view(request, id):
    total_item = get_total_item(request)
    obj = Complect_product.objects.get(id=id)
    similar = Complect_product.objects.all()[::-1]
    category = func_category(request)

    return render(request, template_name='toplarlar_pr_view.html', context={
        'total_item': total_item,
        'products': obj,
        'similarproducts': similar,
        'category': category
    })


#  add to cart  🛒


def add_to_cart(request, id: int):
    print(id)
    cart = request.session.get('cart', {})
    print(cart)
    print(str(id) in cart.keys())
    if str(id) in cart.keys():
        cart.pop(f"{id}")
    else:
        cart[f'{id}'] = 1

    request.session['cart'] = cart
    x = request.POST['next']
    try:
        x = request.POST['next']
    except MultiValueDictKeyError as e:
        return redirect('/' + f'#{id}')
    return redirect(x)


def view_product(request, id: int):
    category = func_category(request)
    product = Product.objects.get(id=id)
    total_item = get_total_item(request)
    print(product.category, 'category')
    similarproducts = Product.objects.filter(category__name=str(product.category))

    return render(request, 'view_product.html', context={
        'category': category,
        'products': product,
        'total_item': total_item,
        'similarproducts': similarproducts
    })


# cart view
def cart_view(request):
    category = func_category(request)
    total_item = get_total_item(request)

    forms = CheckoutForm()
    if request.method == 'POST':
        forms = CheckoutForm(request.POST)
        print(forms.is_valid())
        if forms.is_valid():
            email = forms.cleaned_data['email']
            message = "vash zakazniy nomer 101010"
            # task_send_mail.delay( 'Company Ziyo Nur', message,'settings.EMAIL_HOST_USER',  [email], fail_silently=False )

            forms.save()
            return redirect('cart')

    return render(request, 'cart.html', context={
        'forms': forms,
        'category': category,
        'total_item': total_item

    })

    #
    # if request.method == 'POST':
    #     name = request.POST['name']

#
# def cart_view_view(request):
#     return render(request, 'cart.html')
