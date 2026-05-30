"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from shop.views import (
    home,
    product_detail,
    category_products,
    add_to_cart,
    cart_page,
    decrease_cart_item,
    remove_cart_item,
    checkout_page,
    place_order,
    register_page,
    my_orders,
)
from shop.views import debug_product


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home),
    path("product/<int:product_id>/", product_detail, name="product_detail"),
    path("category/<int:category_id>/", category_products, name="category_products"),
    path("add-to-cart/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("cart/", cart_page, name="cart_page"),
    path(
        "cart/decrease/<str:item_key>/", decrease_cart_item, name="decrease_cart_item"
    ),
    path("cart/remove/<str:item_key>/", remove_cart_item, name="remove_cart_item"),
    path("checkout/", checkout_page, name="checkout_page"),
    path("place-order/", place_order, name="place_order"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="shop/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", register_page, name="register"),
    path("my-orders/", my_orders, name="my_orders"),
    path('debug/<int:pk>/', debug_product),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
