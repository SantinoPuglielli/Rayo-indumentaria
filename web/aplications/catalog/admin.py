from django.contrib import admin
from .models import Categoria, Producto, ProductoVariante, ProductoImagen


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria_padre")
    search_fields = ("nombre",)
    ordering = ("nombre",)


class ProductoVarianteInline(admin.TabularInline):
    model = ProductoVariante
    extra = 1
    fields = ("talle", "color", "stock", "precio_compra", "precio_venta")
    show_change_link = True


class ProductoImagenInline(admin.TabularInline):
    model = ProductoImagen
    extra = 1
    fields = ("color", "imagen", "orden", "imagen_preview")
    readonly_fields = ("imagen_preview",)
    
    def imagen_preview(self, obj):
        if obj.imagen:
            return f'<img src="{obj.imagen.url}" width="80" style="border-radius:5px;" />'
        return "—"
    imagen_preview.allow_tags = True
    imagen_preview.short_description = "Vista previa"


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "get_precio_min", "get_stock_total", "imagen_preview")
    search_fields = ("nombre", "descripcion")
    list_filter = ("categoria",)
    inlines = [ProductoVarianteInline, ProductoImagenInline]
    ordering = ("nombre",)

    def get_precio_min(self, obj):
        variante = obj.variantes.order_by("precio_venta").first()
        return f"${variante.precio_venta}" if variante else "—"
    get_precio_min.short_description = "Precio base"

    def get_stock_total(self, obj):
        total_stock = sum(v.stock for v in obj.variantes.all())
        return total_stock
    get_stock_total.short_description = "Stock total"

    def imagen_preview(self, obj):
        if obj.imagen:
            return f'<img src="{obj.imagen.url}" width="60" style="border-radius:5px;" />'
        return "—"
    imagen_preview.allow_tags = True
    imagen_preview.short_description = "Imagen"


@admin.register(ProductoVariante)
class ProductoVarianteAdmin(admin.ModelAdmin):
    list_display = ("producto", "talle", "color", "stock", "precio_compra", "precio_venta")
    search_fields = ("producto__nombre",)
    list_filter = ("color", "talle", "producto__categoria")
    ordering = ("producto__nombre", "talle", "color")


@admin.register(ProductoImagen)
class ProductoImagenAdmin(admin.ModelAdmin):
    list_display = ("producto", "color", "orden", "imagen_preview")
    list_filter = ("producto", "color")
    search_fields = ("producto__nombre",)
    ordering = ("producto__nombre", "color", "orden")
    
    def imagen_preview(self, obj):
        if obj.imagen:
            return f'<img src="{obj.imagen.url}" width="100" style="border-radius:5px;" />'
        return "—"
    imagen_preview.allow_tags = True
    imagen_preview.short_description = "Vista previa"
