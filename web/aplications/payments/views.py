import json
import decimal
import mercadopago
from django.shortcuts import redirect
from aplications.accounts.models import PerfilUsuario
from aplications.payments.models import MetodoPagoEstado

from django.conf import settings
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required

# Importamos modelos para crear el pedido y el pago
from aplications.orders.models import Pedido, PedidoDetalle
from aplications.payments.models import Pago, MetodoPago


# ===============================================================
# 🔹 CREAR PREFERENCIA (checkout sandbox)
# ===============================================================
from aplications.accounts.models import PerfilUsuario

from aplications.accounts.models import PerfilUsuario
import json, decimal, mercadopago
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

@login_required(login_url="/accounts/login/")
@require_POST
def crear_preferencia(request):
    """
    Guarda el carrito del usuario como PedidoTemporal y crea la preferencia de pago.
    Siempre devuelve un HttpResponse/JsonResponse (nunca None).
    """
    # Import local para evitar ciclos
    from aplications.orders.models import PedidoTemporal

    # 1) Validar carrito
    cart = request.session.get("cart", {})
    if not cart:
        return HttpResponseBadRequest("El carrito está vacío")

    # 2) Obtener perfil del usuario (INSTANCIA, no la clase)
    try:
        perfil_usuario = PerfilUsuario.objects.get(usuario=request.user)
    except PerfilUsuario.DoesNotExist:
        return HttpResponseBadRequest("El usuario no tiene perfil asociado")

    # 3) Persistir carrito como pedido temporal
    try:
        pedido_temp = PedidoTemporal.objects.create(
            usuario=perfil_usuario,             # <— INSTANCIA
            data=json.dumps(cart, ensure_ascii=False),
        )
    except Exception as e:
        return HttpResponseBadRequest(f"No se pudo guardar el pedido temporal: {e}")

    # 4) Armar items e importe total
    items = []
    total_calc = decimal.Decimal("0.00")
    try:
        for variante_id, item in cart.items():
            price = decimal.Decimal(str(item.get("price", 0)))
            qty   = int(item.get("qty", 1))
            name  = item.get("name", f"Producto {variante_id}")
            total_calc += price * qty
            items.append({
                "id": str(variante_id),
                "title": name,
                "quantity": qty,
                "currency_id": "ARS",
                "unit_price": float(price),
            })
    except Exception as e:
        return HttpResponseBadRequest(f"Error armando ítems: {e}")

    if not items:
        return HttpResponseBadRequest("No hay ítems válidos en el carrito")

    # 5) Validaciones básicas de settings
    if not getattr(settings, "MERCADOPAGO_ACCESS_TOKEN", None):
        return HttpResponseBadRequest("Falta MERCADOPAGO_ACCESS_TOKEN en settings")
    if not getattr(settings, "SITE_URL", None):
        return HttpResponseBadRequest("Falta SITE_URL en settings")

    # 6) Crear preferencia en Mercado Pago (con manejo de errores)
    try:
        sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
        preference_data = {
            "items": items,
            "external_reference": str(pedido_temp.id),
            "back_urls": {
                "success": f"{settings.SITE_URL}/pago/retorno/",
                "pending": f"{settings.SITE_URL}/pago/retorno/",
                "failure": f"{settings.SITE_URL}/pago/retorno/",
            },
            "auto_return": "approved",
            "notification_url": f"{settings.SITE_URL}/pago/webhook/",
        }
        result = sdk.preference().create(preference_data)

        # Log útil para depurar
        resp = result.get("response", {}) if isinstance(result, dict) else {}
        init_point = resp.get("init_point")
        status = result.get("status")
        print(f"[MP] status={status} pedido_temp={pedido_temp.id} resp_keys={list(resp.keys())}")

        if not init_point:
            # Devolver info para que podamos ver qué falló
            return HttpResponseBadRequest(f"No se pudo crear la preferencia. Respuesta: {resp}")
        return JsonResponse({"init_point": init_point})
    except Exception as e:
        return HttpResponseBadRequest(f"Error comunicando con Mercado Pago: {e}")


# ===============================================================
# 🔹 WEBHOOK (notificación automática de Mercado Pago)
# ===============================================================
@csrf_exempt
@require_POST
def webhook(request):
    """
    Recibe notificaciones de Mercado Pago y crea el Pedido real cuando el pago se aprueba.
    """
    from aplications.orders.models import Pedido, PedidoDetalle, PedidoTemporal, PedidoEstado
    from aplications.payments.models import MetodoPago, Pago

    try:
        data = json.loads(request.body or "{}")
    except Exception:
        return HttpResponseBadRequest("JSON inválido")

    topic = request.GET.get("type") or data.get("type") or data.get("topic")
    payment_id = (data.get("data") or {}).get("id") or data.get("id")

    if topic != "payment" or not payment_id:
        return HttpResponse("OK")

    sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
    payment = sdk.payment().get(payment_id)["response"]

    status = payment.get("status")
    temp_id = payment.get("external_reference")  # ID del PedidoTemporal
    print(f"[MP] Notificación recibida. status={status}, temp_id={temp_id}")

    pedido_temp = PedidoTemporal.objects.filter(pk=temp_id).first()
    if not pedido_temp:
        print("[MP] ❌ Pedido temporal no encontrado.")
        return HttpResponse("Pedido temporal no encontrado")

    cart = json.loads(pedido_temp.data)
    perfil = pedido_temp.usuario

    # ✅ Si tu modelo Pedido espera un User:
    usuario = perfil.usuario

    if status == "approved":
        total_calc = decimal.Decimal("0.00")
        for item in cart.values():
            total_calc += decimal.Decimal(item["price"]) * int(item["qty"])

        # obtener o crear estado “Pagado”
        estado_pagado, _ = PedidoEstado.objects.get_or_create(nombre="Pagado", tipo="finalizado")

        # crear pedido con el usuario real
        pedido = Pedido.objects.create(
            usuario=usuario,  # ✅ ahora es User, no PerfilUsuario
            fecha=timezone.now(),
            total=total_calc,
            estado=estado_pagado,
            direccion="—",
        )

        # crear detalles
        for variante_id, item in cart.items():
            PedidoDetalle.objects.create(
                pedido=pedido,
                variante_id=variante_id,
                cantidad=item["qty"],
                precio_unitario=item["price"],
            )

        estado_activo, _ = MetodoPagoEstado.objects.get_or_create(nombre="Activo")
        
        # ✅ obtener o crear el método con estado válido
        metodo, _ = MetodoPago.objects.get_or_create(
            nombre="Mercado Pago (Sandbox)",
            defaults={"estado": estado_activo},
        )

        # si ya existía pero no tenía estado asignado, lo actualizamos
        if not metodo.estado_id:
            metodo.estado = estado_activo
            metodo.save(update_fields=["estado"])
            
            
        # crear registro de pago
        Pago.objects.create(
            pedido=pedido,
            metodo_pago=metodo,
            monto=pedido.total,
            fecha_pago=timezone.now(),
        )


        # ✅ limpiar pedido temporal
        pedido_temp.delete()

        # ✅ limpiar carrito si existe (solo si hay sesión abierta)
        try:
            if hasattr(request, "session") and "cart" in request.session:
                del request.session["cart"]
                request.session.modified = True
                print("[MP] 🧹 Carrito vaciado tras pago aprobado.")
        except Exception as e:
            print(f"[MP] ⚠️ No se pudo limpiar carrito: {e}")

        print(f"[MP] ✅ Pedido {pedido.id} creado correctamente.")

    return HttpResponse("OK")



# ===============================================================
# 🔹 RETORNO (pantalla al volver del checkout)
# ===============================================================
@require_GET
def retorno(request):
    """
    Pantalla de retorno al volver de Mercado Pago.
    Se ejecuta en el navegador del usuario, así que podemos vaciar el carrito de la sesión.
    """
    status = request.GET.get("status", "pending")

    # 🧹 Vaciar carrito de sesión si existe
    if "cart" in request.session:
        del request.session["cart"]
        request.session.modified = True
        print("[RETORNO] 🧹 Carrito vaciado al retornar del pago.")

    # 🔁 Redirigir según estado del pago
    if status == "approved":
        # Podés mostrar una plantilla de “pago exitoso” si querés
        return redirect("/")  # o redirect("gracias") si tenés esa vista
    elif status == "pending":
        return redirect("/")  # o a una vista de “pago pendiente”
    else:
        return redirect("/")  # o a una vista de “pago fallido”

