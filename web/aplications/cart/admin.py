from django.contrib import admin
from .models import CarritoEstado

@admin.register(CarritoEstado)
class CarritoEstadoAdmin(admin.ModelAdmin):
    list_display = ("id", "tipo")
    search_fields = ("tipo",)
    ordering = ("tipo",)

# ❌ Ocultamos Carrito y CarritoItem del admin
from .models import Carrito, CarritoItem
try:
    admin.site.unregister(Carrito)
except admin.sites.NotRegistered:
    pass
try:
    admin.site.unregister(CarritoItem)
except admin.sites.NotRegistered:
    pass
