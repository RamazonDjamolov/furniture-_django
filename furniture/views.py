from django.shortcuts import render, redirect
from .forms import CheckoutForm
from django.utils.datastructures import MultiValueDictKeyError

from django.conf import settings
from django.http import HttpResponse
from .models import *
from .tasks import send_email_task, send_email_admin_task


def checkout(request):
    cart = request.session.get('cart')
    cart2 = request.session.get('cart2')
    order = Order.objects.latest('id')
    for k, v in cart.items():
        oreder_item = OrderItem.objects.create(product=Product.objects.get(id=k), quantity=v, order=order).save()

    for k, v in cart2.items():
        oreder_item = OrderItem.objects.create(comlect=Complect_product.objects.get(id=k), quantity=v,
                                               order=order).save()

    request.session['cart'] = {}
    request.session['cart2'] = {}
    print()


def func_category(request):
    categories = Category.objects.all()
    return categories


def get_total_item(request):
    cart = request.session.get('cart', {})
    cart2 = request.session.get('cart2', {})
    x = sum(cart.values())
    s = sum(cart2.values())
    return x + s


def main(request):
    category = func_category(request)
    total_item = get_total_item(request)
    prodct =Product.objects.all()[::4]
    return render(request, 'main.html', {
        'category': category,
        'total_item': total_item,
        
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


#  add to cart  ++++


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


#  add toplamlar
def add_to_cart_toplam(request, id: int):
    print(id)
    cart2 = request.session.get('cart2', {})
    print(cart2)
    print(str(id) in cart2.keys())
    if str(id) in cart2.keys():
        cart2.pop(f"{id}")
    else:
        cart2[f'{id}'] = 1

    request.session['cart2'] = cart2
    print(request.session['cart2'], 'cart2')
    x = request.POST['next']
    try:
        x = request.POST['next']
    except MultiValueDictKeyError as e:
        return redirect('/' + f'#{id}')
    return redirect(x)


#  view product 👁👁👁👁👁
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


# toplar view 👀👀👀👀👀
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


#  toplarlar pagenini viewsi
def toplam_view(request):
    total_item = get_total_item(request)
    obj = Complect_product.objects.all()
    category = func_category(request)
    return render(request, template_name='toplamlar.html', context={
        'total_item': total_item,
        'products': obj,
        'category': category
    })


# cart view  🛒🛒🛒🛒🛒🛒🛒
def cart_view(request):
    category = func_category(request)
    total_item = get_total_item(request)
    cart = request.session['cart']
    cart2 = request.session['cart2']
    products = Product.objects.all().filter(id__in=cart.keys())
    toplam = Complect_product.objects.all().filter(id__in=cart2.keys())
    s = []
    total_price = 0
    total_sale = 0
    for k, v in cart.items():
        for j in products:
            if j.id == int(k):
                s.append((j, v, int(v) * float(j.real_price)))
                total_price += float(v) * float(j.real_price)
                total_sale += float(v) * float(0 if j.sale_price == None else j.sale_price)

    for k, v in cart2.items():
        for j in toplam:
            if j.id == int(k):
                s.append((j, v, int(v) * float(j.real_price)))
                total_price += float(v) * float(j.real_price)
                total_sale += float(v) * float(0 if j.sale_price == None else j.sale_price)

    forms = CheckoutForm()
    if request.method == 'POST':
        forms = CheckoutForm(request.POST)
        print(forms.is_valid())
        if forms.is_valid():
            email = forms.cleaned_data['email']
            user = forms.cleaned_data['full_name']
            phone_number = forms.cleaned_data['phone_number']
            forms.save()
            send_email_task.delay(str(email))
            send_email_admin_task.delay(str(user), phone_number, [i[0].name for i in s],
                                        [i[0].img.first().img.url for i in s])

            checkout(request)
            return redirect('cart')

    return render(request, 'cart.html', context={
        'forms': forms,
        'category': category,
        'total_item': total_item,
        'products': s,
        'total_price': total_price,
        'total_sale': total_sale

    })


def add(request, id):
    x = request.GET.get('next', '/')
    cart = request.session.get('cart', {})
    s = cart.get(str(id))
    print(s, "object ")
    cart.update({str(id): s + 1})
    request.session['cart'] = cart

    return redirect(x + f'#{id}')


def sub(request, id):
    x = request.GET.get('next', '/')
    cart = request.session.get('cart', {})

    s = cart.get(str(id))
    if s != 1:
        cart.update({str(id): s - 1})
    request.session['cart'] = cart
    return redirect(x + f'#{id}')


def delete(request, id):
    cart = request.session.get('cart')
    s = cart.pop(str(id))
    request.session['cart'] = cart
    return redirect('cart')


def delete_top(request, id):
    cart2 = request.session.get('cart2')
    s = cart2.pop(str(id))
    request.session['cart2'] = cart2
    return redirect('cart')


def add_top(request, id):
    x = request.GET.get('next', '/')
    cart2 = request.session.get('cart2', {})
    s = cart2.get(str(id))
    print(s, "object ")
    cart2.update({str(id): s + 1})
    request.session['cart2'] = cart2

    return redirect(x + f'#komplekt{id}')


def sub_top(request, id):
    x = request.GET.get('next', '/')
    cart2 = request.session.get('cart2', {})
    s = cart2.get(str(id))
    if s != 1:
        cart2.update({str(id): s - 1})
    request.session['cart2'] = cart2
    return redirect(x + f'#komplekt{id}')
