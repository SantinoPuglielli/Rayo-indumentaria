from django.contrib import admin
from .models import Pedido, PedidoDetalle


class PedidoDetalleInline(admin.TabularInline):
    model = PedidoDetalle
    extra = 0
    fields = ("variante", "cantidad", "precio_unitario")
    show_change_link = True


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "fecha", "estado_coloreado", "get_total")
    list_filter = ("estado", "fecha")
    search_fields = ("usuario__nombre", "usuario__email")
    inlines = [PedidoDetalleInline]
    ordering = ("-fecha",)
    list_per_page = 25

    def estado_coloreado(self, obj):
        colores = {
            "PENDIENTE": "orange",
            "PAGADO": "green",
            "CANCELADO": "red",
            "ENVIADO": "blue",
            "COMPLETADO": "gray",
        }
        color = colores.get(obj.estado.upper(), "black")
        return f'<b style="color:{color}">{obj.estado}</b>'
    estado_coloreado.allow_tags = True
    estado_coloreado.short_description = "Estado"

    def get_total(self, obj):
        total = sum(detalle.cantidad * detalle.precio_unitario for detalle in obj.detalles.all())
        return f"${total:,.2f}"
    get_total.short_description = "Total"


@admin.register(PedidoDetalle)
class PedidoDetalleAdmin(admin.ModelAdmin):
    list_display = ("pedido", "variante", "cantidad", "precio_unitario", "get_subtotal")
    search_fields = ("pedido__usuario__nombre", "variante__producto__nombre")
    list_filter = ("pedido__estado", "pedido__fecha")

    def get_subtotal(self, obj):
        return f"${obj.cantidad * obj.precio_unitario:,.2f}"
    get_subtotal.short_description = "Subtotal"
