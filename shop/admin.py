from django.contrib import admin
from .models import (
    Product,
    Category,
    Order,
    OrderItem,
    ProductImage,
    ProductVariant,
    VariantImage,
)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


class VariantImageInline(admin.TabularInline):
    model = VariantImage
    extra = 1


class ProductVariantAdmin(admin.ModelAdmin):
    inlines = [VariantImageInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductVariantInline, ProductImageInline]


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
admin.site.register(ProductVariant, ProductVariantAdmin)
admin.site.register(VariantImage)
