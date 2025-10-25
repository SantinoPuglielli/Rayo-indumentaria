from decimal import Decimal, InvalidOperation

from django.shortcuts import render
from django.db.models import Q, Prefetch
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from .models import Favorito



# Modelos en español
from .models import (
    Producto,
    Categoria,
    ProductoVariante,
    ProductoImagen,  # Importado el nuevo modelo
)


def _to_decimal(value, default=None):
    if value in (None, ""):
        return default
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return default


def product_list(request):
    q = (request.GET.get("q") or "").strip()
    pmin = _to_decimal(request.GET.get("pmin"))
    pmax = _to_decimal(request.GET.get("pmax"))

    selected_cats = request.GET.getlist("category")
    selected_colors = request.GET.getlist("color")
    selected_sizes = request.GET.getlist("size")

    qs = (
        Producto.objects
        .select_related("categoria")
        .prefetch_related(
            Prefetch("variantes", queryset=ProductoVariante.objects.all())
        )
        .all()
    )

    if q:
        qs = qs.filter(
            Q(nombre__icontains=q)
            | Q(descripcion__icontains=q)
            | Q(categoria__nombre__icontains=q)
        )

    if pmin is not None:
        qs = qs.filter(variantes__precio_venta__gte=pmin)
    if pmax is not None:
        qs = qs.filter(variantes__precio_venta__lte=pmax)

    if selected_cats:
        qs = qs.filter(categoria_id__in=selected_cats)
    if selected_colors:
        qs = qs.filter(variantes__color__in=selected_colors)
    if selected_sizes:
        qs = qs.filter(variantes__talle__in=selected_sizes)

    qs = qs.distinct()

    paginator = Paginator(qs, 12)
    products = paginator.get_page(request.GET.get("page"))

    # Agregamos atributo para saber si cada producto está en favoritos
    if request.user.is_authenticated:
        favoritos_ids = set(
            Favorito.objects.filter(usuario=request.user).values_list("producto_id", flat=True)
        )
        for producto in products:
            producto.es_favorito = producto.id in favoritos_ids
    else:
        for producto in products:
            producto.es_favorito = False

    categories = list(Categoria.objects.all())
    colors = list(
        ProductoVariante.objects.values_list("color", flat=True).distinct().order_by("color")
    )
    sizes = list(
        ProductoVariante.objects.values_list("talle", flat=True).distinct().order_by("talle")
    )

    for c in categories:
        setattr(c, "slug", str(c.id))

    ctx = {
        "products": products,
        "q": q,
        "pmin": "" if pmin is None else str(pmin),
        "pmax": "" if pmax is None else str(pmax),
        "categories": categories,
        "colors": colors,
        "sizes": sizes,
        "selected_cats": set(selected_cats),
        "selected_colors": set(selected_colors),
        "selected_sizes": set(selected_sizes),
    }

    return render(request, "catalog/product_list.html", ctx)

from django.shortcuts import get_object_or_404

def product_detail(request, pk):
    producto = get_object_or_404(
        Producto.objects.select_related("categoria").prefetch_related("variantes", "imagenes"),
        pk=pk
    )

    variantes = ProductoVariante.objects.filter(producto=producto)
    relacionados = (
        Producto.objects.filter(categoria=producto.categoria)
        .exclude(pk=producto.pk)
        .select_related("categoria")[:4]
    )

    imagenes_por_color = {}
    imagenes_generales = []
    
    for img in producto.imagenes.all():
        if img.color:
            if img.color not in imagenes_por_color:
                imagenes_por_color[img.color] = []
            imagenes_por_color[img.color].append(img)
        else:
            imagenes_generales.append(img)

    # Verificar si el producto está en favoritos
    es_favorito = False
    if request.user.is_authenticated:
        es_favorito = Favorito.objects.filter(usuario=request.user, producto=producto).exists()

    ctx = {
        "producto": producto,
        "variantes": variantes,
        "relacionados": relacionados,
        "es_favorito": es_favorito,
        "imagenes_por_color": imagenes_por_color,  # Agregado al contexto
        "imagenes_generales": imagenes_generales,  # Agregado al contexto
    }

    return render(request, "catalog/product_detail.html", ctx)

@login_required
def toggle_favorito(request, pk):
    """Agrega o quita un producto de la lista de favoritos"""
    producto = get_object_or_404(Producto, pk=pk)
    favorito, creado = Favorito.objects.get_or_create(usuario=request.user, producto=producto)

    if not creado:
        favorito.delete()
        messages.info(request, f"❌ {producto.nombre} fue eliminado de tus favoritos.")
    else:
        messages.success(request, f"❤️ {producto.nombre} fue agregado a tus favoritos.")

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def favoritos_view(request):
    """Muestra todos los productos que el usuario marcó como favoritos"""
    favoritos = Favorito.objects.filter(usuario=request.user).select_related("producto")
    return render(request, "accounts/favoritos.html", {"favoritos": favoritos})
