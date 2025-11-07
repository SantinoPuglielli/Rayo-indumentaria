from django.shortcuts import render, redirect, get_object_or_404
from aplications.catalog.models import ProductoVariante
from django.http import JsonResponse
from django.views.decorators.http import require_POST


# 🛒 Mostrar carrito
def cart_view(request):
    cart = request.session.get('cart', {})
    if not isinstance(cart, dict):
        cart = {}

    items = []
    total = 0

    for variante_id, item in cart.items():
        subtotal = item['price'] * item['qty']
        total += subtotal
        items.append({
            'id': variante_id,
            'name': item['name'],
            'price': item['price'],
            'qty': item['qty'],
            'subtotal': subtotal,
            'image': item.get('image'),  # ✅ agregar imagen al contexto
        })

    return render(request, 'cart/cart.html', {'cart': items, 'total': total})


# ➕ Agregar producto al carrito
@require_POST
def add_to_cart(request, variante_id):
    variante = get_object_or_404(ProductoVariante, pk=variante_id)
    cart = request.session.get('cart', {})

    if not isinstance(cart, dict):
        cart = {}

    key = str(variante_id)
    if key in cart:
        cart[key]['qty'] += 1
    else:
        cart[key] = {
            'name': f"{variante.producto.nombre} ({variante.talle}, {variante.color})",
            'price': float(variante.precio_venta),
            'qty': 1,
            'image': variante.producto.imagen.url if variante.producto.imagen else '/static/img/no-image.png',  # ✅ imagen agregada
        }

    request.session['cart'] = cart
    request.session.modified = True

    # 🔧 Respuesta JSON para fetch o redirección normal
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.headers.get('Accept') == 'application/json':
        total_items = sum(item['qty'] for item in cart.values())
        return JsonResponse({'success': True, 'total_items': total_items})

    return redirect('cart:view')


# ➖ Eliminar un producto del carrito
def remove_from_cart(request, variante_id):
    cart = request.session.get('cart', {})
    key = str(variante_id)
    if key in cart:
        del cart[key]
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('cart:view')


# 🔄 Vaciar carrito
def clear_cart(request):
    request.session['cart'] = {}
    request.session.modified = True
    return redirect('cart:view')


# 🔼 Incrementar cantidad de producto
def increase_qty(request, variante_id):
    cart = request.session.get('cart', {})
    key = str(variante_id)
    if key in cart:
        cart[key]['qty'] += 1
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('cart:view')


# 🔽 Disminuir cantidad de producto
def decrease_qty(request, variante_id):
    cart = request.session.get('cart', {})
    key = str(variante_id)
    if key in cart:
        cart[key]['qty'] -= 1
        if cart[key]['qty'] <= 0:
            del cart[key]
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('cart:view')


# 🗑️ Restar una unidad (dar de baja parcial)
def remove_one(request, variante_id):
    cart = request.session.get('cart', {})
    key = str(variante_id)

    if key in cart:
        cart[key]['qty'] -= 1
        if cart[key]['qty'] <= 0:
            del cart[key]
        request.session['cart'] = cart
        request.session.modified = True

    return redirect('cart:view')

def cart_count(request):
    cart = request.session.get('cart', {})
    if not isinstance(cart, dict):
        cart = {}
    total_items = sum(item['qty'] for item in cart.values())
    return JsonResponse({'total_items': total_items})