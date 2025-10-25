from django.db import models
from django.conf import settings

class PedidoEstado(models.Model):
    nombre = models.CharField(max_length=50)
    tipo = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Estado de pedido"
        verbose_name_plural = "Estados de pedido"
        unique_together = (("nombre", "tipo"),)
        ordering = ["tipo", "nombre"]

    def __str__(self):
        return f"{self.tipo} - {self.nombre}"


class Pedido(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="pedidos")
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.ForeignKey(PedidoEstado, on_delete=models.PROTECT, related_name="pedidos")
    total = models.DecimalField(max_digits=12, decimal_places=2)
    direccion = models.CharField(max_length=255)
    numero_factura = models.CharField(max_length=50, unique=True, null=True, blank=True)

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        indexes = [
            models.Index(fields=["usuario", "fecha"], name="idx_pedido_usuario_fecha"),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(total__gte=0), name="ck_pedido_total_gte_0"),
        ]
        ordering = ["-fecha"]

    def __str__(self):
        return f"Pedido #{self.pk} - {self.usuario}"


class PedidoDetalle(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="detalles")
    variante = models.ForeignKey("catalog.ProductoVariante", on_delete=models.PROTECT, related_name="pedido_detalles")
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = "Detalle de pedido"
        verbose_name_plural = "Detalles de pedido"
        indexes = [
            models.Index(fields=["pedido"], name="idx_pdet_pedido"),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(cantidad__gt=0), name="ck_pdet_cantidad_gt_0"),
            models.CheckConstraint(
                check=(models.Q(precio_unitario__isnull=True) | models.Q(precio_unitario__gte=0)),
                name="ck_pdet_pu_null_or_gte_0",
            ),
        ]

    def __str__(self):
        return f"{self.pedido} - {self.variante} x {self.cantidad}"


