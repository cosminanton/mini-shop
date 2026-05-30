from django.shortcuts import render, get_object_or_404, redirect
from .models import Order, Product, Category, OrderItem
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from urllib.parse import quote, unquote


def get_cart_count(request):
    cart = request.session.get("cart", {})

    if isinstance(cart, list):
        return len(cart)

    total = 0

    for item in cart.values():
        if isinstance(item, dict):
            total += item.get("quantity", 0)
        else:
            total += item

    return total


def home(request):
    categories = Category.objects.all()
    query = request.GET.get("q")
    cart_count = get_cart_count(request)

    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    return render(
        request,
        "shop/home.html",
        {
            "products": products,
            "categories": categories,
            "selected_category": None,
            "query": query,
            "cart_count": cart_count,
        },
    )


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_count = get_cart_count(request)
    
    colors = product.variants.exclude(color="").values_list("color", flat=True).distinct()
    sizes = product.variants.exclude(size="").values_list("size", flat=True).distinct()
    types = product.variants.exclude(variant_type="").values_list("variant_type", flat=True).distinct()
    

    return render(
        request,
        "shop/product_detail.html",
        {"product": product, "cart_count": cart_count, "colors": colors, "sizes": sizes, "types": types},
    )


def category_products(request, category_id):
    categories = Category.objects.all()
    selected_category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=selected_category)
    cart_count = get_cart_count(request)

    return render(
        request,
        "shop/home.html",
        {
            "products": products,
            "categories": categories,
            "selected_category": selected_category,
            "cart_count": cart_count,
        },
    )


def add_to_cart(request, product_id):
    cart = request.session.get("cart", {})

    if isinstance(cart, list):
        cart = {}

    color = request.POST.get("color", "")
    size = request.POST.get("size", "")
    variant_type = request.POST.get("variant_type", "")

    cart_key = f"{product_id}|{color}|{size}|{variant_type}"

    cart[cart_key] = {
        "product_id": product_id,
        "quantity": cart.get(cart_key, {}).get("quantity", 0) + 1,
        "color": color,
        "size": size,
        "variant_type": variant_type,
    }

    request.session["cart"] = cart

    return redirect(request.META.get("HTTP_REFERER", "/"))


def decrease_cart_item(request, item_key):
    item_key = unquote(item_key)
    cart = request.session.get("cart", {})

    if item_key in cart:
        if isinstance(cart[item_key], dict):
            cart[item_key]["quantity"] -= 1

            if cart[item_key]["quantity"] <= 0:
                del cart[item_key]
        else:
            cart[item_key] -= 1

            if cart[item_key] <= 0:
                del cart[item_key]

    request.session["cart"] = cart

    return redirect("cart_page")


def remove_cart_item(request, item_key):
    item_key = unquote(item_key)
    cart = request.session.get("cart", {})

    if isinstance(cart, list):
        cart = {}

    if item_key in cart:
        del cart[item_key]

    request.session["cart"] = cart

    return redirect("cart_page")


def cart_page(request):
    cart = request.session.get("cart", {})

    cart_items = []
    total = 0

    for key, item in cart.items():
        product = get_object_or_404(Product, id=item["product_id"])
        quantity = item["quantity"]
        subtotal = product.price * quantity
        total += subtotal

        cart_items.append({
            "key": key,
            "url_key": quote(key, safe=""),
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal,
            "color": item.get("color"),
            "size": item.get("size"),
            "variant_type": item.get("variant_type"),
        })

    return render(request, "shop/cart.html", {
        "cart_items": cart_items,
        "total": total,
        "cart_count": sum(item["quantity"] for item in cart.values()),
    })


@login_required
def checkout_page(request):
    cart_count = get_cart_count(request)

    return render(request, "shop/checkout.html", {"cart_count": cart_count})


@login_required
def place_order(request):
    cart = request.session.get("cart", {})

    if not cart:
        return redirect("cart_page")

    products = Product.objects.filter(id__in=cart.keys())

    total = 0

    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    email = request.POST.get("email")
    address = request.POST.get("address")
    city = request.POST.get("city")
    postal_code = request.POST.get("postal_code")

    order = Order.objects.create(
        user=request.user,
        first_name=first_name,
        last_name=last_name,
        email=email,
        address=address,
        city=city,
        postal_code=postal_code,
        total_price=0,
    )

    for product in products:
        quantity = cart[str(product.id)]
        if product.stock < quantity:
            return redirect("cart_page")
        subtotal = product.price * quantity
        total += subtotal

        OrderItem.objects.create(
            order=order, product=product, quantity=quantity, price=product.price
        )
        product.stock -= quantity
        product.save()

    order.total_price = total
    order.save()

    request.session["cart"] = {}

    return render(request, "shop/order_confirmation.html", {"order": order})


def register_page(request):

    if request.method == "POST":

        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        user = User.objects.create_user(
            username=username, email=email, password=password
        )

        login(request, user)

        return redirect("/")

    return render(request, "shop/register.html")


@login_required
def my_orders(request):
    if not request.user.is_authenticated:
        return redirect("login")

    orders = Order.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "shop/my_orders.html", {"orders": orders})
