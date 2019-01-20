from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.template.defaulttags import register
from .models import Product


class ProductListView(generic.ListView):
    "Main view, display a list of products to buy"
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

    def get_context_data(self, **kwargs):
        "Add to context"
        context = super(generic.ListView, self).get_context_data(**kwargs)
        context['cart'] = {'tesla car': 1}
        return context


def cart(request):
    request.session.modified = True
    try:
        product_to_add = Product.objects.get(pk=request.GET['product_id'][0])
    except:
        HttpResponse("Unknown error")

    if request.session.get('cart') is None:
        request.session['cart'] = {}

    if request.session.get('cart').get(product_to_add.title) is None:
        request.session['cart'][product_to_add.title] = 1
    else:
        request.session['cart'][product_to_add.title] += 1

    @register.filter
    def get_index(List, i):
        return List[int(i)]

    def get_price_from_title(title):
        try:
            return Product.objects.get(title=title).price
        except:
            return 0

    def total(cart):
        total = 0
        for item_name,amount in cart.items():
            price = get_price_from_title(item_name)
            total += price * amount
        return total

    price_list = [
        get_price_from_title(title) for title in request.session['cart']
    ]
    context = {
        'price_list': price_list,
        'total': total(request.session['cart'])
    }

    return render(request, 'simplemarketplaceapp/cart.html', context)


def detail(request, pk):
    product = Product.objects.get(pk=pk)
    context = {
        'product': product,
    }
    cart = request.GET.get('cart')
    if cart:
        context['cart'] = cart

    if product.isAvailable():
        product.inventory_count -= 1
        product.save()
        context['purchaseSuccessful'] = True
    else:
        context['purchaseSuccessful'] = False

    return render(request, 'simplemarketplaceapp/product_detail.html', context)

def confim_purchase(request):
    if request.session.get('cart') is None:
        text = "Your cart is empty"

    else:
        # Validate that transaction is possible
        for item,amount in request.session['cart'].items:
            product = Product.objects.get(title=item)
            if product.inventory_count < amount:
                text = """
                Some items in your cart are not available anymore
                The order was cancelled, sorry for the inconvenience
                """
                break
        # Execute transaction
        for item,amount in request.session['cart'].items:
            product = Product.objects.get(title=item)
            product.inventory_count -= amount
        text = """
        Your order is complete,
        Thank you
        """
    return render(requets, 'purchase.html', {
        'text': text
    })
