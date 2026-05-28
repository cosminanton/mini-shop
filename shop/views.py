from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from django.contrib.auth.models import User
from django.contrib.auth import login


def get_cart_count(request):
    cart = request.session.get('cart', {})

    if isinstance(cart, list):
        return len(cart)

    return sum(cart.values())


def home(request):
    categories = Category.objects.all()
    query = request.GET.get('q')
    cart_count = get_cart_count(request)

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
    cart_count = get_cart_count(request)

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'cart_count': cart_count
    })


def category_products(request, category_id):
    categories = Category.objects.all()
    selected_category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=selected_category)
    cart_count = get_cart_count(request)

    return render(request, 'shop/home.html', {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'cart_count': cart_count
    })


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    if isinstance(cart, list):
        cart = {}

    product_id = str(product_id)
    cart[product_id] = cart.get(product_id, 0) + 1

    request.session['cart'] = cart

    return redirect(request.META.get('HTTP_REFERER', '/'))


def decrease_cart_item(request, product_id):
    cart = request.session.get('cart', {})

    if isinstance(cart, list):
        cart = {}

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] -= 1

        if cart[product_id] <= 0:
            del cart[product_id]

    request.session['cart'] = cart

    return redirect('cart_page')


def remove_cart_item(request, product_id):
    cart = request.session.get('cart', {})

    if isinstance(cart, list):
        cart = {}

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart

    return redirect('cart_page')


def cart_page(request):
    cart = request.session.get('cart', {})

    if isinstance(cart, list):
        cart = {}

    products = Product.objects.filter(id__in=cart.keys())

    cart_items = []
    total = 0

    for product in products:
        quantity = cart[str(product.id)]
        subtotal = product.price * quantity
        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'total': total,
        'cart_count': sum(cart.values())
    })

def checkout_page(request):
    cart_count = get_cart_count(request)

    return render(request, 'shop/checkout.html', {
        'cart_count': cart_count
    })

def place_order(request):
    request.session['cart'] = {}

    return render(request, 'shop/order_confirmation.html')

def register_page(request):

    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)

        return redirect('/')

    return render(request, 'shop/register.html')