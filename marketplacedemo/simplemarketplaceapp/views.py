from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import Product


class ProductListView(generic.ListView):
    model = Product
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

    def process_response(self, request, response):
        response['Cache-Control'] = 'no-cache, must-revalidate, no-store'
        response['Pragma'] = 'no-cache'
        return response

def detail(request, pk):

    product = Product.objects.get(pk=pk)
    context = {
        'product': product,
    }
    if product.isAvailable():
        product.inventory_count -= 1
        product.save()
        context['purchaseSuccessful'] = True
    else:
        context['purchaseSuccessful'] = False

    return render(request, 'simplemarketplaceapp/product_detail.html', context)
