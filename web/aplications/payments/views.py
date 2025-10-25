from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_POST
import mercadopago

def _cart_from_session(request):
    """
    Devuelve la estructura del carrito guardado en sesión.
    Espera algo tipo:
    {
      "4": {"id": 4, "name": "camisa (xl, rojo)", "qty": 1, "price": "2222.00"},
      ...
    }
    """
    cart = request.session.get('cart')  # clave que usa tu app del carrito
    return cart if isinstance(cart, dict) and cart else {}

def _mp_items(cart):
    items = []
    total = 0.0
    for pid, it in cart.items():
        qty = int(it.get('qty', 1))
        price = float(it.get('price', 0))
        name = it.get('name', 'Producto')
        if qty <= 0 or price <= 0:
            continue
        total += qty * price
        items.append({
            "title": name,
            "quantity": qty,
            "unit_price": round(price, 2),
            "currency_id": "ARS",
        })
    return items, round(total, 2)

@require_POST
def mp_create(request):
    # 1) Leer carrito de la sesión
    cart = _cart_from_session(request)
    if not cart:
        return JsonResponse({"error": "El carrito está vacío."}, status=400)

    # 2) Armar ítems para MP
    items, total = _mp_items(cart)
    if not items:
        return JsonResponse({"error": "No hay ítems válidos en el carrito."}, status=400)

    # 3) Instanciar SDK con tu ACCESS TOKEN (sandbox)
    sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

    # 4) Dominio público actual (ngrok)
    public_url = "https://florine-carcanetted-unmalevolently.ngrok-free.dev/"  # ⚠️ CAMBIA esto por tu dominio actual de ngrok

    # 5) Back URLs completas
    success_url = f"{public_url}/payments/success/"
    failure_url = f"{public_url}/payments/failure/"
    pending_url = f"{public_url}/payments/pending/"

    preference_data = {
        "items": items,
        "back_urls": {
            "success": success_url,
            "failure": failure_url,
            "pending": pending_url,
        },
        "auto_return": "approved",
    }

    try:
        pref = sdk.preference().create(preference_data)
        if pref.get("status") != 201:
            print("⚠️ Error en la respuesta de Mercado Pago:", pref)
            msg = pref.get("message") or pref.get("error") or "Error creando la preferencia"
            return JsonResponse({"error": msg}, status=500)

        init_point = pref["response"]["sandbox_init_point"]
        return JsonResponse({"init_point": init_point})
    except Exception as e:
        print(f"❌ Excepción creando preferencia: {e}")
        return JsonResponse({"error": f"Excepción creando preferencia: {e}"}, status=500)

# Vistas de retorno (pueden ser simples por ahora)
from django.shortcuts import render

def success_view(request):
    return render(request, 'payments/success.html')

def failure_view(request):
    return render(request, 'payments/failure.html')

def pending_view(request):
    return render(request, 'payments/pending.html')
