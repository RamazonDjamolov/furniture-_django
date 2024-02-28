from django.shortcuts import render
from .forms import checkoutForm


def main(request):

    return render(request, 'main.html')


def cart_view(request):
    # order_id =
    forms = checkoutForm()
    if request.method == 'POST':
        forms = checkoutForm(request.POST)
        if forms.is_valid():
            forms.save()


    return render(request, 'cart.html', context={'forms': forms})

    #
    # if request.method == 'POST':
    #     name = request.POST['name']



def category_view(request):
    return render(request, 'category.html')


#
# def cart_view_view(request):
#     return render(request, 'cart.html')