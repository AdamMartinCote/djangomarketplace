from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    fields = [
        'title',
        'price',
        'inventory_count',
    ]
