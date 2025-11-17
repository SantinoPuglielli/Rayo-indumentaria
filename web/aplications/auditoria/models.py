from django.db import models
from django.contrib.auth.models import User

class Auditoria(models.Model):
    ACCIONES = [
        ('CREAR', 'Creación'),
        ('EDITAR', 'Edición'),
        ('ELIMINAR', 'Eliminación'),
        ('LOGIN', 'Inicio de sesión'),
        ('LOGOUT', 'Cierre de sesión'),
        ('CAMBIO_ESTADO', 'Cambio de estado'),
        ('PEDIDO', 'Creación de pedido'),
        ('PAGO', 'Registro de pago'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    accion = models.CharField(max_length=50, choices=ACCIONES)
    fecha = models.DateTimeField(auto_now_add=True)
    tabla_afectada = models.CharField(max_length=100)
    registro_id = models.IntegerField(null=True, blank=True)
    detalle = models.TextField(null=True, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        verbose_name = "Registro de Auditoría"
        verbose_name_plural = "Registros de Auditoría"
        ordering = ['-fecha']

    def __str__(self):
        return f"[{self.fecha.strftime('%d/%m/%Y %H:%M')}] {self.usuario} - {self.accion} ({self.tabla_afectada})"
