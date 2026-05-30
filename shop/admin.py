from django.contrib import admin
from .models import Product, Category, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


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


# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
