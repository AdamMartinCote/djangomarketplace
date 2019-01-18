from django.shortcuts import render
from django.views import generic
from .models import Product


class ProductListView(generic.ListView):
    model = Product
    # template_name = 'productList.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        query = self.request.GET.get('filter')
        onlyAvailable = self.request.GET.get('onlyAvailable')
        if query and onlyAvailable:
            return Product.objects.filter(title__icontains=query,
                                          inventory_count__gt=0)
        elif query:
            return Product.objects.filter(title__icontains=query)
        elif onlyAvailable:
            return Product.objects.filter(inventory_count__gt=0)
        else:
            return Product.objects.all()

class DetailView(generic.DetailView):
    model = Product
    # template_name = 'product_details.html'
