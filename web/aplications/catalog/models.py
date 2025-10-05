from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    def __str__(self): return self.name

class Size(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    def __str__(self): return self.name

class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    hex = models.CharField(max_length=7, blank=True, help_text="#RRGGBB (opcional)")
    def __str__(self): return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    is_active = models.BooleanField(default=True)
    sizes = models.ManyToManyField(Size, blank=True, related_name="products")
    colors = models.ManyToManyField(Color, blank=True, related_name="products")

    def __str__(self): 
        return self.name

    def main_image_url(self):
        """
        Devuelve la URL de la primera imagen (o None si no tiene).
        Útil para listados.
        """
        first = self.images.order_by('order', 'id').first()
        return first.image.url if first and first.image else None

class ProductImage(models.Model):
    """
    Galería de imágenes por producto (N imágenes por producto).
    """
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/%Y/%m/%d/')
    is_main = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"Imagen de {self.product.name} ({self.id})"
