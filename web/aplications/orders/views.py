from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Pedido, PedidoDetalle, PedidoEstado
from aplications.cart.models import CarritoItem
from aplications.accounts.models import PerfilUsuario


@login_required
def crear_pedido(request):
    """
    Crea un nuevo pedido a partir del carrito del usuario.
    Copia automáticamente la dirección del perfil.
    """
    try:
        perfil = PerfilUsuario.objects.get(usuario=request.user)
    except PerfilUsuario.DoesNotExist:
        return HttpResponseForbidden("No se encontró un perfil asociado al usuario.")

    # Estado inicial del pedido (por ejemplo: 'Pendiente')
    estado_inicial = PedidoEstado.objects.filter(nombre__iexact="Pendiente").first()
    if not estado_inicial:
        estado_inicial = PedidoEstado.objects.create(nombre="Pendiente", tipo="Inicial")

    # Crear el pedido
    pedido = Pedido.objects.create(
        usuario=request.user,
        estado=estado_inicial,
        total=0,
        direccion=perfil.direccion,
    )

    # Obtener los productos del carrito
    carrito_items = CarritoItem.objects.filter(usuario=request.user)

    for item in carrito_items:
        PedidoDetalle.objects.create(
            pedido=pedido,
            variante=item.variante,
            cantidad=item.cantidad,
            precio_unitario=item.variante.precio_venta,
        )

    # Calcular el total del pedido
    pedido.calcular_total()

    # Vaciar el carrito
    carrito_items.delete()

    # Redirigir al detalle del pedido
    return redirect("orders:detalle_pedido", pedido_id=pedido.id)


@login_required
def detalle_pedido(request, pedido_id):
    """
    Muestra los detalles de un pedido específico.
    - Los usuarios comunes solo pueden ver sus propios pedidos.
    - Los administradores (is_staff o superuser) pueden ver todos los pedidos.
    """
    pedido = get_object_or_404(Pedido, pk=pedido_id)

    # 🔒 Si no es admin, solo puede ver su propio pedido
    if not request.user.is_staff and not request.user.is_superuser:
        if pedido.usuario != request.user:
            return HttpResponseForbidden("No tenés permiso para ver este pedido.")

    detalles = PedidoDetalle.objects.filter(pedido=pedido)

    context = {
        "pedido": pedido,
        "detalles": detalles,
    }
    return render(request, "orders/detalle_pedido.html", context)
