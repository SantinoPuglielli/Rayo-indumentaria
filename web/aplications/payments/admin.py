from django.contrib import admin
from .models import MetodoPagoEstado, MetodoPago

@admin.register(MetodoPagoEstado)
class MetodoPagoEstadoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)
    ordering = ("nombre",)


@admin.register(MetodoPago)
class MetodoPagoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "estado")
    list_filter = ("estado",)
    search_fields = ("nombre",)
    ordering = ("nombre",)
