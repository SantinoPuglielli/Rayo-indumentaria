from django.contrib import admin
from django import forms
from .models import (
    Categoria,
    Producto,
    ProductoVariante,
    ProductoImagen,
    Talle,
    Color
)

# -------------------------------------------
# 🧾 Formularios personalizados
# -------------------------------------------
class ProductoVarianteForm(forms.ModelForm):
    talle = forms.ModelChoiceField(queryset=Talle.objects.all(), required=True, label="Talle")
    color = forms.ModelChoiceField(queryset=Color.objects.all(), required=False, label="Color")

    class Meta:
        model = ProductoVariante
        fields = "__all__"


# -------------------------------------------
# 🗂️ Categorías
# -------------------------------------------
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria_padre")
    search_fields = ("nombre",)
    ordering = ("nombre",)
    verbose_name_plural = "Categorías"


# -------------------------------------------
# 📸 Inlines dentro de Producto
# -------------------------------------------
class ProductoVarianteInline(admin.TabularInline):
    model = ProductoVariante
    form = ProductoVarianteForm
    extra = 1
    fields = ("talle", "color", "stock", "precio_compra", "precio_venta")
    show_change_link = False


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


# -------------------------------------------
# 👕 Productos
# -------------------------------------------
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "categoria",
        "get_precio_min",
        "get_stock_total",
        "imagen_preview",
    )
    search_fields = ("nombre", "descripcion")
    list_filter = ("categoria",)
    inlines = [ProductoVarianteInline, ProductoImagenInline]
    ordering = ("nombre",)
    list_per_page = 25

    # 🔹 Ocultamos Talle y Color del formulario principal
    fields = ("nombre", "descripcion", "categoria", "imagen")

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
    imagen_preview.short_description = "Imagen principal"


# -------------------------------------------
# 🧹 Ocultamos modelos secundarios del menú
# -------------------------------------------
for model in (ProductoVariante, ProductoImagen):
    try:
        admin.site.unregister(model)
    except admin.sites.NotRegistered:
        pass


# -------------------------------------------
# 📏 Referencias (Talle y Color)
# -------------------------------------------
@admin.register(Talle)
class TalleAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)
    ordering = ("nombre",)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "codigo_hex")
    search_fields = ("nombre",)
    ordering = ("nombre",)
