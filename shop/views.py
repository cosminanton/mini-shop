from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    return render(request, 'shop/home.html', {
        'products': products,
        'categories': categories,
        'selected_category': None

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


