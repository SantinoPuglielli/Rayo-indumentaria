from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CarouselSlide(models.Model):
    title = models.CharField("Título", max_length=120, blank=True)
    subtitle = models.CharField("Subtítulo", max_length=200, blank=True)
    image = models.ImageField("Imagen", upload_to='carousel/')
    # CharField para permitir rutas internas como /catalog/
    button_text = models.CharField("Texto del botón", max_length=50, blank=True, default='Ver más')
    button_url = models.CharField("Botón URL o ruta", max_length=300, blank=True, default="/catalog/")
    is_active = models.BooleanField("Activo", default=True)
    order = models.PositiveIntegerField("Orden", default=0)

    class Meta:
        ordering = ['order','id']
        verbose_name = "Slide de carrusel"
        verbose_name_plural = "Slides de carrusel"
    db_table = 'core_carouselslide'  # nombre creado por migraciones locales
    managed = True

    def __str__(self):
        return self.title or f"Slide {self.id}"

    def clean(self):
        if self.button_url and not (
            self.button_url.startswith(('http://','https://','/'))
        ):
            raise ValidationError({'button_url': 'Usá http(s)://... o una ruta que empiece con “/”'})
        





from django.db import models

class Usuario(models.Model):
    """
    Modelo que mapea a la tabla Usuario existente en SQL Server.
    NO hereda de AbstractBaseUser para evitar conflictos con auth.User
    """
    id_usuario = models.AutoField(primary_key=True, db_column='ID_Usuario')
    nombre = models.CharField(max_length=100, db_column='Nombre')
    apellido = models.CharField(max_length=100, db_column='Apellido')
    email = models.EmailField(unique=True, db_column='Email')
    contrasenia = models.CharField(max_length=255, db_column='Contrasenia')
    id_rol = models.IntegerField(default=2, db_column='ID_Rol')  # 1=Admin, 2=Usuario
    direccion = models.CharField(max_length=255, db_column='Direccion')
    telefono = models.CharField(max_length=20, blank=True, null=True, db_column='Telefono')
    id_estado_usuario = models.IntegerField(default=1, db_column='ID_EstadoUsuario')
    
    class Meta:
        managed = False  # Django NO creará esta tabla
        db_table = 'Usuario'  # Nombre exacto de tu tabla en SQL Server
    
    @property
    def is_admin(self):
        """Verifica si el usuario es administrador (rol = 1)"""
        return self.id_rol == 1
    
    @property
    def is_active(self):
        """Verifica si el usuario está activo (estado = 1)"""
        return self.id_estado_usuario == 1
    
    def _str_(self):
        return f"{self.nombre} {self.apellido} ({self.email})"