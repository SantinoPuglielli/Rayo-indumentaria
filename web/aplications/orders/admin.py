from django.contrib import admin
from .models import Pedido, PedidoDetalle


# -------------------------------------------
# 🔒 Solo lectura y vista detallada de pedidos
# -------------------------------------------
class PedidoDetalleInline(admin.TabularInline):
    model = PedidoDetalle
    extra = 0
    can_delete = False
    readonly_fields = (
        "get_producto",
        "get_talle",
        "get_color",
        "cantidad",
        "precio_unitario",
        "get_subtotal",
    )
    show_change_link = False

    def get_producto(self, obj):
        return obj.variante.producto.nombre
    get_producto.short_description = "Producto"

    def get_talle(self, obj):
        return obj.variante.talle
    get_talle.short_description = "Talle"

    def get_color(self, obj):
        return obj.variante.color
    get_color.short_description = "Color"

    def get_subtotal(self, obj):
        if obj.precio_unitario is not None:
            return f"${obj.cantidad * obj.precio_unitario:,.2f}"
        return "—"
    get_subtotal.short_description = "Subtotal"


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "usuario",
        "estado",
        "total",
        "direccion",
        "fecha",
        "numero_factura",
    )
    list_filter = ("estado", "fecha")
    search_fields = ("usuario__username", "numero_factura", "direccion")
    inlines = [PedidoDetalleInline]
    ordering = ("-fecha",)
    readonly_fields = (
        "usuario",
        "estado",
        "total",
        "direccion",
        "numero_factura",
        "fecha",
    )

    # ❌ Bloqueamos agregar, editar o eliminar
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    # 🔹 Quitamos acción “eliminar seleccionados”
    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions


@admin.register(PedidoDetalle)
class PedidoDetalleAdmin(admin.ModelAdmin):
    list_display = (
        "pedido",
        "get_producto",
        "get_talle",
        "get_color",
        "cantidad",
        "precio_unitario",
        "get_subtotal",
    )
    search_fields = ("pedido__id", "variante__producto__nombre")
    ordering = ("-pedido",)
    readonly_fields = (
        "pedido",
        "get_producto",
        "get_talle",
        "get_color",
        "cantidad",
        "precio_unitario",
        "get_subtotal",
    )

    def get_producto(self, obj):
        return obj.variante.producto.nombre
    get_producto.short_description = "Producto"

    def get_talle(self, obj):
        return obj.variante.talle
    get_talle.short_description = "Talle"

    def get_color(self, obj):
        return obj.variante.color
    get_color.short_description = "Color"

    def get_subtotal(self, obj):
        if obj.precio_unitario is not None:
            return f"${obj.cantidad * obj.precio_unitario:,.2f}"
        return "—"
    get_subtotal.short_description = "Subtotal"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
