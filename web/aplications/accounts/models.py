from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

class UsuarioEstado(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Estado de usuario"
        verbose_name_plural = "Estados de usuario"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Funcion(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Función"
        verbose_name_plural = "Funciones"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class RolFuncion(models.Model):
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, related_name="rol_funciones")
    funcion = models.ForeignKey(Funcion, on_delete=models.CASCADE, related_name="funcion_roles")

    class Meta:
        verbose_name = "Rol - Función"
        verbose_name_plural = "Roles - Funciones"
        unique_together = (("rol", "funcion"),)


class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="perfil")
    estado = models.ForeignKey(UsuarioEstado, on_delete=models.PROTECT, related_name="usuarios")
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=30, blank=True)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT, related_name="usuarios")

    class Meta:
        verbose_name = "Perfil de usuario"
        verbose_name_plural = "Perfiles de usuario"

    def __str__(self):
        return f"{self.usuario} ({self.rol})"



