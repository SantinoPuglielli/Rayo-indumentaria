from django.db import models

class MetodoPagoEstado(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Estado de método de pago"
        verbose_name_plural = "Estados de método de pago"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class MetodoPago(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    estado = models.ForeignKey(MetodoPagoEstado, on_delete=models.PROTECT, related_name="metodos")

    class Meta:
        verbose_name = "Método de pago"
        verbose_name_plural = "Métodos de pago"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Pago(models.Model):
    pedido = models.ForeignKey("orders.Pedido", on_delete=models.CASCADE, related_name="pagos")
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.PROTECT, related_name="pagos")
    fecha_pago = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        indexes = [
            models.Index(fields=["pedido"], name="idx_pago_pedido"),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(monto__gte=0), name="ck_pago_monto_gte_0"),
        ]
        ordering = ["-fecha_pago"]

    def __str__(self):
        return f"Pago #{self.pk} - {self.metodo_pago} - ${self.monto}"


