from django.shortcuts import render, get_object_or_404
from .models import Product

def home(request):
    """
    Контроллер главной страницы
    """
    products = Product.objects.all()
    context = {'object_list': products}
    return render(request, 'catalog/home.html', context)

def contacts(request):
    """
    Контроллер страницы контактов
    """
    return render(request, 'catalog/contacts.html')

def product_detail(request, pk):
    """
    Контроллер страницы товара.
    """
    product = get_object_or_404(Product, pk=pk)
    context = {'object': product}
    return render(request, 'catalog/product_detail.html', context)