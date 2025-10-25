from django.db import models
from django.conf import settings

class CarritoEstado(models.Model):
    tipo = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Estado de carrito"
        verbose_name_plural = "Estados de carrito"
        ordering = ["tipo"]

    def __str__(self):
        return self.tipo


class Carrito(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="carritos")
    estado = models.ForeignKey(CarritoEstado, on_delete=models.PROTECT, related_name="carritos")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Carrito"
        verbose_name_plural = "Carritos"
        indexes = [
            models.Index(fields=["usuario", "fecha_creacion"], name="idx_carrito_usuario_fecha"),
        ]

    def __str__(self):
        return f"Carrito #{self.pk} de {self.usuario}"


class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name="items")
    variante = models.ForeignKey("catalog.ProductoVariante", on_delete=models.PROTECT, related_name="carrito_items")
    cantidad = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Ítem de carrito"
        verbose_name_plural = "Ítems de carrito"
        unique_together = (("carrito", "variante"),)
        indexes = [
            models.Index(fields=["carrito"], name="idx_citem_carrito"),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(cantidad__gt=0), name="ck_citem_cantidad_gt_0"),
        ]

    def __str__(self):
        return f"{self.variante} x {self.cantidad}"


