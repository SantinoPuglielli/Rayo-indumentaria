from django.urls import path
from django.shortcuts import render
from django.db.utils import ProgrammingError, OperationalError
from django.db.models import F
from aplications.catalog.models import Producto
from . import views

def home(request):
    """
    Página principal: muestra los productos destacados automáticamente
    según su popularidad (clics, favoritos, compras, agregados al carrito).
    Si la base todavía no está lista, evita que se caiga el sitio.
    """
    featured = []

    try:
        featured = Producto.objects.annotate(
            score=F('clics') + F('agregados_carrito') * 2 + F('compras') * 3 + F('favoritos') * 2
        ).order_by('-score')[:12]
    except (ProgrammingError, OperationalError, Exception):
        # Si la tabla todavía no existe (por ejemplo, antes de migrar), se evita el error
        pass

    return render(request, 'core/home.html', {'featured': featured})

urlpatterns = [
    path('', home, name='home'),
    path('preguntas-frecuentes/', views.preguntas_frecuentes, name='preguntas_frecuentes'),
    path('envios-devoluciones/', views.envios_devoluciones, name='envios_devoluciones'),
    path('politica-privacidad/', views.politica_privacidad, name='politica_privacidad'),
    path('terminos-condiciones/', views.terminos_condiciones, name='terminos_condiciones'),
]

