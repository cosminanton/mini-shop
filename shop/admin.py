from django.contrib import admin
from .models import Product, Category, Order, OrderItem, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]

    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "total_price",
        "created_at",
    )

    list_filter = ("created_at",)

    search_fields = (
        "first_name",
        "last_name",
        "email",
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(ProductImage)
