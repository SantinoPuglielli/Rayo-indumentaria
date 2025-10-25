from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    categoria_padre = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL, related_name="subcategorias"
    )

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="productos")
    imagen = models.ImageField(upload_to="productos/", blank=True, null=True)

    # 🔥 Campos de popularidad (nuevos)
    clics = models.PositiveIntegerField(default=0)
    agregados_carrito = models.PositiveIntegerField(default=0)
    compras = models.PositiveIntegerField(default=0)
    favoritos = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        indexes = [
            models.Index(fields=["categoria"], name="idx_producto_categoria"),
        ]
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

    def popularidad(self):
        """
        Calcula un puntaje de popularidad basado en la interacción del usuario.
        Se usa para decidir qué productos se muestran en la sección de destacados.
        """
        return self.clics + (self.agregados_carrito * 2) + (self.compras * 3) + (self.favoritos * 2)


class ProductoVariante(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="variantes")
    talle = models.CharField(max_length=20)
    color = models.CharField(max_length=50)
    stock = models.PositiveIntegerField(default=0)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Variante de producto"
        verbose_name_plural = "Variantes de producto"
        unique_together = (("producto", "talle", "color"),)
        indexes = [
            models.Index(fields=["producto"], name="idx_var_producto"),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(stock__gte=0), name="ck_var_stock_gte_0"),
            models.CheckConstraint(check=models.Q(precio_compra__gte=0), name="ck_var_pc_gte_0"),
            models.CheckConstraint(check=models.Q(precio_venta__gte=0), name="ck_var_pv_gte_0"),
        ]
        ordering = ["producto__nombre", "talle", "color"]

    def __str__(self):
        return f"{self.producto} - {self.talle} - {self.color}"


class ProductoImagen(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="imagenes")
    color = models.CharField(max_length=50, blank=True, null=True, help_text="Dejar vacío para imagen general del producto")
    imagen = models.ImageField(upload_to="productos/galeria/")
    orden = models.PositiveIntegerField(default=0, help_text="Orden de aparición en el carrusel")
    
    class Meta:
        verbose_name = "Imagen de producto"
        verbose_name_plural = "Imágenes de productos"
        ordering = ["producto", "color", "orden"]
    
    def __str__(self):
        if self.color:
            return f"{self.producto.nombre} - {self.color} - Imagen {self.orden}"
        return f"{self.producto.nombre} - Imagen general {self.orden}"


class Favorito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favoritos")
    # ⚙️ FIX: cambiado el related_name para evitar conflicto con Producto.favoritos
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="favoritos_rel")
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'producto')
        verbose_name = "Favorito"
        verbose_name_plural = "Favoritos"

    def __str__(self):
        return f"{self.usuario.username} - {self.producto.nombre}"
