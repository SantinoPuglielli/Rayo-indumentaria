from django.contrib import admin
from .models import PerfilUsuario, UsuarioEstado

@admin.register(UsuarioEstado)
class UsuarioEstadoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)
    ordering = ("nombre",)


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ("usuario", "rol", "estado", "telefono")
    list_filter = ("rol", "estado")
    search_fields = ("usuario__username", "usuario__email", "telefono", "direccion")
    ordering = ("usuario",)

# ❌ Ocultamos Rol, Funcion y RolFuncion del admin
from .models import Rol, Funcion, RolFuncion
for model in (Rol, Funcion, RolFuncion):
    try:
        admin.site.unregister(model)
    except admin.sites.NotRegistered:
        pass
