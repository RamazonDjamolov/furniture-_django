from django.shortcuts import render, redirect
from .forms import CheckoutForm
from django.utils.datastructures import MultiValueDictKeyError

from django.conf import settings
from django.http import HttpResponse
from .models import *
from .tasks import send_email_task, send_email_admin_task
from django.db.models import Q


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


def func_complect_category(request):
    xonalar = Xonalar.objects.all()
    print(xonalar, "XONALAR")
    return xonalar


def get_total_item(request):
    cart = request.session.get('cart', {})
    cart2 = request.session.get('cart2', {})
    x = sum(cart.values())
    s = sum(cart2.values())
    return x + s


def main(request):
    category = func_category(request)
    xonalar = func_complect_category(request)
    total_item = get_total_item(request)
    prodct = Product.objects.all()[::4]
    return render(request, 'main.html', {
        'category': category,
        'total_item': total_item,
        'xonalar': xonalar,
        'products': prodct

    })


# categoriyaga tegishli bolgan hamma narsalarni boshlanishi


def product_category(request, id: int):
    products = Product.objects.all().filter(category_id=id).all()
    category = func_category(request)
    total_item = get_total_item(request)
    xonalar = func_complect_category(request)

    return render(request, 'category.html', context={
        'products': products,
        'category': category,
        'xonalar': xonalar,
        'total_item': total_item
    })


def new_product(request):
    category = func_category(request)
    xonalar = func_complect_category(request)
    try:
        products = Product.objects.all()[::20]
    except:
        products = Product.objects.all()
    total_item = get_total_item(request)
    return render(request, 'category.html', {
        'category': category,
        'products': products,
        'total_item': total_item,
        'xonalar': xonalar,

    })


def products_main(request, name):
    total_item = get_total_item(request)
    category = func_category(request)
    xonalar = func_complect_category(request)
    try:
        obj = Complect_product.objects.all().filter(xonalar__name=name)
        return render(request, 'toplamlar.html', context={
            'total_item': total_item,
            'products': obj,
            'category': category,
            'xonalar': xonalar
        })
    except:
        obj = Product.objects.all().filter(category__name=name)
        return render(request, 'category.html', {
            'total_item': total_item,
            'products': obj,
            'category': category,
            'xonalar': xonalar
        })
        print(obj, "obj 2222222")


def category_view(request):
    category = func_category(request)
    xonalar = func_complect_category(request)
    products = Product.objects.all()
    total_item = get_total_item(request)
    return render(request, 'category.html', {
        'category': category,
        'products': products,
        'total_item': total_item,
        'xonalar': xonalar,

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


def add_to_cart2(request, id: int):
    cart = request.session.get('cart', {})
    if request.method == "POST":
        qu = request.POST['quantity']

        try:
            cart.update({f'{id}': int(qu)})
        except:
            cart.update({f'{id}': int(1)})

    request.session['cart'] = cart
    try:
        x = request.POST['next']
    except MultiValueDictKeyError as e:
        return redirect('/' + f'#{id}')
    return redirect(x)


#  add toplamlar
def add_to_cart_toplam(request, id: int):
    print(id)
    cart2 = request.session.get('cart2', {})
    print(str(id) in cart2.keys())
    if str(id) in cart2.keys():
        cart2.pop(f"{id}")
    else:
        cart2[f'{id}'] = 1

    request.session['cart2'] = cart2
    try:
        x = request.POST['next']
    except MultiValueDictKeyError as e:
        return redirect('/' + f'#{id}')
    return redirect(x)


def add_to_cart_toplam2(request, id: int):
    cart2 = request.session.get('cart2', {})

    if request.method == "POST":
        qu = request.POST['quantity']
        s = cart2.get(str(id))
        print(id, 'product_ctoplam_category2  id', 'qunatity == ', qu)
        try:
            if str(id) in cart2.keys():
                cart2.update({f'{id}': s + int(qu)})
            else:
                cart2[f'{id}'] = int(qu)

        except:
            cart2[f'{id}'] = 1

    request.session['cart2'] = cart2
    try:
        x = request.POST['next']
    except MultiValueDictKeyError as e:
        return redirect('/' + f'#{id}')
    return redirect(x)


#  view product 👁👁👁👁👁
def view_product(request, id: int):
    xonalar = func_complect_category(request)

    category = func_category(request)
    try:
        product = Product.objects.get(id=id)
    except:
        return redirect('main')
    total_item = get_total_item(request)
    similarproducts = Product.objects.filter(category__name=str(product.category))

    return render(request, 'view_product.html', context={
        'category': category,
        'products': product,
        'total_item': total_item,
        'similarproducts': similarproducts,
        'xonalar': xonalar,
    })


# toplar view 👀👀👀👀👀
def toplam_pr_view(request, id):
    total_item = get_total_item(request)
    try:
        obj = Complect_product.objects.get(id=id)
    except:
        return redirect('main')
    similar = Complect_product.objects.all()[::-1]
    category = func_category(request)
    xonalar = func_complect_category(request)

    return render(request, template_name='toplarlar_pr_view.html', context={
        'total_item': total_item,
        'products': obj,
        'similarproducts': similar,
        'category': category,
        'xonalar': xonalar
    })


#  toplarlar pagenini viewsi
def toplam_view(request, id: int):
    total_item = get_total_item(request)
    obj = Complect_product.objects.all().filter(xonalar__id=id)
    category = func_category(request)
    xonalar = func_complect_category(request)

    return render(request, template_name='toplamlar.html', context={
        'total_item': total_item,
        'products': obj,
        'category': category,
        'xonalar': xonalar
    })


# cart view  🛒🛒🛒🛒🛒🛒🛒
def cart_view(request):
    category = func_category(request)
    total_item = get_total_item(request)
    xonlar = func_complect_category(request)
    try:
        cart = request.session['cart']
        cart2 = request.session['cart2']
    except KeyError:
        w = request.session.get('cart', {})
        w1 = request.session.get('cart2', {})
        request.session['cart'] = w
        request.session['cart2'] = w1
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
            print(email, "dilferuz ")
            user = forms.cleaned_data['full_name']
            phone_number = forms.cleaned_data['phone_number']
            forms.save()

            send_email_task.delay(str(email))
            imgs = []
            for i in s:
                try:
                    imgs.append(i[0].img.first().img.url)
                except:
                    imgs.append(i[0].product.first().img.first().img.url)

            send_email_admin_task.delay(str(user), phone_number, [i[0].name for i in s], f"imgages == {imgs}")

            checkout(request)
            return redirect('cart')

    return render(request, 'cart.html', context={
        'forms': forms,
        'category': category,
        'total_item': total_item,
        'products': s,
        'total_price': total_price,
        'total_sale': total_sale,
        'xonalar': xonlar,

    })


#  cart + - delete m
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


# search

def search(request):
    category = func_category(request)
    total_item = get_total_item(request)
    xonalar = func_complect_category(request)
    if request.method == "GET":
        q = request.GET.get('q', '')
        s = []

        toplam = Complect_product.objects.filter(Q(name__icontains=q)).all()
        products = Product.objects.filter(Q(name__icontains=q) | Q(category__name__icontains=q)).all()
        for i in toplam:
            s.append(i)
        for i in products:
            s.append(i)
        print(s)

    return render(request, template_name='search.html', context={
        'products': s,
        'category': category,
        'total_item': total_item,
        'xonalar': xonalar,

    })
