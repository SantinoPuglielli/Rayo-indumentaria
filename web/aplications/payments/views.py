from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponseForbidden

from aplications.accounts.models import PerfilUsuario
from aplications.orders.models import Pedido, PedidoDetalle, PedidoEstado
# Usamos el carrito que está guardado en sesión, no el modelo CarritoItem


@login_required(login_url="/accounts/login/")
def pago_transferencia(request):
    """
    Genera un Pedido a partir del carrito en sesión y muestra
    una pantalla con los datos para pagar por transferencia bancaria.
    """
    # 1) Obtener carrito desde la sesión
    cart = request.session.get("cart", {})
    if not isinstance(cart, dict) or not cart:
        # Si no hay carrito, lo mandamos al listado de productos o al carrito
        return redirect("cart:view")

    # 2) Obtener perfil del usuario para usar dirección
    try:
        perfil = PerfilUsuario.objects.get(usuario=request.user)
        direccion = perfil.direccion or "Sin dirección especificada"
    except PerfilUsuario.DoesNotExist:
        # Si no hay perfil, podemos bloquear o usar un fallback
        return HttpResponseForbidden(
            "No se encontró un perfil asociado al usuario. "
            "Por favor, completá tus datos en la sección Mi perfil."
        )

    # 3) Estado inicial del pedido: 'Pendiente de pago'
    estado_pendiente, _ = PedidoEstado.objects.get_or_create(
        nombre="Pendiente de pago",
        tipo="inicial",
    )

    # 4) Calcular total y crear Pedido
    total = Decimal("0.00")
    for item in cart.values():
        price = Decimal(str(item.get("price", 0)))
        qty = int(item.get("qty", 1))
        total += price * qty

    pedido = Pedido.objects.create(
        usuario=request.user,
        fecha=timezone.now(),
        estado=estado_pendiente,
        total=total,
        direccion=direccion,
    )

    # 5) Crear los detalles del pedido
    for variante_id, item in cart.items():
        PedidoDetalle.objects.create(
            pedido=pedido,
            variante_id=variante_id,
            cantidad=int(item.get("qty", 1)),
            precio_unitario=Decimal(str(item.get("price", 0))),
        )

    # 6) Vaciar carrito de sesión
    if "cart" in request.session:
        del request.session["cart"]
        request.session.modified = True

    # 7) Renderizar pantalla de datos de transferencia
    # 🔴 Acá poné los datos REALES del cliente
    context = {
        "pedido": pedido,
        "total": total,
        "perfil": perfil,
        "cbu": "0000003100033491289794",
        "alias": "RAYO.INDUMENTARIA",
        "titular": "RAYO INDUMENTARIA SRL",
    }
    return render(request, "payments/pago_transferencia.html", context)
