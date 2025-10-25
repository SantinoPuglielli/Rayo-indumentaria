from django.shortcuts import render
from aplications.catalog.models import Producto
from django.db.models import F

def home(request):
    """
    Página principal del sitio: muestra los productos destacados automáticamente
    según su popularidad (clics, favoritos, compras, agregados al carrito)
    """
    featured = Producto.objects.annotate(
        score=F('clics') + F('agregados_carrito') * 2 + F('compras') * 3 + F('favoritos') * 2
    ).order_by('-score')[:12]

    return render(request, 'core/home.html', {'featured': featured})

from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')

def preguntas_frecuentes(request):
    return render(request, 'core/preguntas_frecuentes.html')

def envios_devoluciones(request):
    return render(request, 'core/envios_devoluciones.html')

def politica_privacidad(request):
    return render(request, 'core/politica_privacidad.html')

def terminos_condiciones(request):
    return render(request, 'core/terminos_condiciones.html')
