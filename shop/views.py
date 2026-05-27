from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category


def home(request):
    categories = Category.objects.all()
    query = request.GET.get('q')
    cart = request.session.get('cart', [])
    cart_count = len(cart)

    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    return render(request, 'shop/home.html', {
        'products': products,
        'categories': categories,
        'selected_category': None,
        'query': query,
        'cart_count': cart_count
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    return render(request, 'shop/product_detail.html', {
        'product': product
    })


def category_products(request, category_id):
    categories = Category.objects.all()

    selected_category = get_object_or_404(Category, id=category_id)

    products = Product.objects.filter(category=selected_category)

    return render(request, 'shop/home.html', {
        'products': products,
        'categories': categories,
        'selected_category': selected_category
    })

def add_to_cart(request, product_id):
    cart = request.session.get('cart', [])

    if product_id not in cart:
        cart.append(product_id)

    request.session['cart'] = cart

    return redirect('/')


