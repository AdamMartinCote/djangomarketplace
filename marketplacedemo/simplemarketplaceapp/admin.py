from django.contrib import admin
from django.contrib.sessions.models import Session

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    fields = [
        'title',
        'price',
        'inventory_count',
    ]


admin.site.register(Session)
