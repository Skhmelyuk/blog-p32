from django.shortcuts import render, get_object_or_404
from .models import Product
from main.models import Category

def product_list(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()

    return render(request, 'shop/product_list.html', {
        'products': products,
        'categories': categories,
        'title': 'Наші Товари'
    })

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, is_active=True)
    categories = Category.objects.all()

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'categories': categories,
        'title': product.name
    })

