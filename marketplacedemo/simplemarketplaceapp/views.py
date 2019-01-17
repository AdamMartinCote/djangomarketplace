from django.shortcuts import render
from django.views.generic import ListView
from .models import Product


class ProductListView(ListView):
    model = Product
    template_name = 'productList.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        query = self.request.GET.get('filter')
        if query:
            return Product.objects.filter(title__icontains=query)
        else:
            return Product.objects.all()
