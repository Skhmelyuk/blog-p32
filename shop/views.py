from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .models import Product
from .cart import Cart
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

# Представлення додавання товару
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    # Отримуємо кількість з форми (якщо передано)
    quantity = int(request.POST.get('quantity', 1))
    override = request.POST.get('override', False)
    
    cart.add(product=product, quantity=quantity, override_quantity=override)
    return redirect('shop:cart_detail')

# Представлення видалення товару
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('shop:cart_detail')

# Детальна сторінка кошика
def cart_detail(request):
    cart = Cart(request)
    categories = Category.objects.all()
    return render(request, 'shop/cart_detail.html', {
        'cart': cart, 
        'categories': categories,
        'title': 'Кошик покупця'
    })


