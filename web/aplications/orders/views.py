from django.shortcuts import render, get_object_or_404
from .models import Pedido, PedidoDetalle

def detalle_pedido(request, pedido_id):
    """
    Muestra los detalles de un pedido específico.
    Solo accesible si el pedido pertenece al usuario actual.
    """
    pedido = get_object_or_404(Pedido, pk=pedido_id)

    # ⚠️ Seguridad: solo el dueño del pedido puede verlo
    if pedido.usuario != request.user:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("No tenés permiso para ver este pedido.")

    detalles = PedidoDetalle.objects.filter(pedido=pedido)

    context = {
        'pedido': pedido,
        'detalles': detalles,
    }
    return render(request, 'orders/detalle_pedido.html', context)
