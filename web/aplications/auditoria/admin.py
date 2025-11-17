from django.contrib import admin
from .models import Auditoria

@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'usuario', 'accion', 'tabla_afectada', 'registro_id')
    list_filter = ('accion', 'tabla_afectada', 'usuario')
    search_fields = ('usuario__username', 'accion', 'tabla_afectada', 'detalle')
    readonly_fields = ('fecha', 'usuario', 'accion', 'tabla_afectada', 'registro_id', 'detalle', 'ip')
    ordering = ('-fecha',)

    # ❌ No se permite agregar registros manualmente
    def has_add_permission(self, request):
        return False

    # ❌ No se permite modificar registros existentes
    def has_change_permission(self, request, obj=None):
        return False

    # ❌ No se permite borrar registros
    def has_delete_permission(self, request, obj=None):
        return False
