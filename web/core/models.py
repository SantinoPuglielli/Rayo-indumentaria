from django.db import models
from django.core.exceptions import ValidationError

class CarouselSlide(models.Model):
    title = models.CharField("Título", max_length=120, blank=True)
    subtitle = models.CharField("Subtítulo", max_length=200, blank=True)
    image = models.ImageField("Imagen", upload_to='carousel/')
    # CharField para permitir rutas internas como /catalog/
    button_text = models.CharField("Texto del botón", max_length=50, blank=True, default='Ver más')
    button_url = models.CharField("Botón URL o ruta", max_length=300, blank=True, default="/catalog/")
    is_active = models.BooleanField("Activo", default=True)
    order = models.PositiveIntegerField("Orden", default=0)

    class Meta:
        ordering = ['order','id']
        verbose_name = "Slide de carrusel"
        verbose_name_plural = "Slides de carrusel"

    def __str__(self):
        return self.title or f"Slide {self.id}"

    def clean(self):
        if self.button_url and not (
            self.button_url.startswith(('http://','https://','/'))
        ):
            raise ValidationError({'button_url': 'Usá http(s)://... o una ruta que empiece con “/”'})
