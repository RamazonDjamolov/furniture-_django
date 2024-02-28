from django.shortcuts import render, redirect
from .forms import CheckoutForm


def main(request):
    return render(request, 'main.html')


def cart_view(request):
    forms = CheckoutForm()
    if request.method == 'POST':
        forms = CheckoutForm(request.POST)
        print("ddddddddddddddddddddd")
        print(forms.is_valid())
        if forms.is_valid():
            print(forms.cleaned_data)
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
