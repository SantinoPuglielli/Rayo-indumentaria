from django.shortcuts import render, redirect, get_object_or_404
from aplications.catalog.models import Product
from .utils import get_cart, save_cart
from django.views.decorators.http import require_POST

def detail(request):
    cart = get_cart(request)
    total = sum(i['price']*i['qty'] for i in cart)
    return render(request, 'cart/detail.html', {'cart': cart, 'total': total})

@require_POST
def add(request, pk):
    p = get_object_or_404(Product, pk=pk)
    cart = get_cart(request)
    for line in cart:
        if line['id'] == p.id:
            line['qty'] += 1
            save_cart(request, cart)
            return redirect('cart:detail')
    cart.append({'id': p.id, 'name': p.name, 'price': float(p.price), 'qty': 1})
    save_cart(request, cart)
    return redirect('cart:detail')
