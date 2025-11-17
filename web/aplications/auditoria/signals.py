from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from aplications.auditoria.models import Auditoria
from aplications.catalog.models import Producto
from aplications.orders.models import Pedido

# 🔹 Producto


# 🔹 Pedido
@receiver(post_save, sender=Pedido)
def log_pedido_guardado(sender, instance, created, **kwargs):
    accion = 'PEDIDO' if created else 'EDITAR'
    Auditoria.objects.create(
        usuario=instance.usuario if instance.usuario_id else None,
        accion=accion,
        tabla_afectada='Pedido',
        registro_id=instance.id,
        detalle=f"Pedido #{instance.id} {'creado' if created else 'modificado'} por {instance.usuario}"
    )

@receiver(post_delete, sender=Pedido)
def log_pedido_eliminado(sender, instance, **kwargs):
    Auditoria.objects.create(
        usuario=instance.usuario if instance.usuario_id else None,
        accion='ELIMINAR',
        tabla_afectada='Pedido',
        registro_id=instance.id,
        detalle=f"Pedido eliminado #{instance.id}"
    )
