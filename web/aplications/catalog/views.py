from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Product, Category, Color, Size

def product_list(request):
    q = request.GET.get('q','').strip()
    pmin = request.GET.get('pmin')
    pmax = request.GET.get('pmax')
    selected_cats   = request.GET.getlist('category')  # slugs
    selected_colors = request.GET.getlist('color')     # slugs
    selected_sizes  = request.GET.getlist('size')      # slugs

    qs = Product.objects.filter(is_active=True).select_related('category').prefetch_related('colors','sizes','images')

    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q) | Q(category__name__icontains=q))
    if pmin:
        qs = qs.filter(price__gte=pmin)
    if pmax:
        qs = qs.filter(price__lte=pmax)
    if selected_cats:
        qs = qs.filter(category__slug__in=selected_cats)
    if selected_colors:
        qs = qs.filter(colors__slug__in=selected_colors).distinct()
    if selected_sizes:
        qs = qs.filter(sizes__slug__in=selected_sizes).distinct()

    paginator = Paginator(qs, 12)
    products = paginator.get_page(request.GET.get('page'))

    ctx = {
        "products": products,
        "q": q, "pmin": pmin or "", "pmax": pmax or "",
        "categories": Category.objects.all(),
        "colors": Color.objects.all(),
        "sizes": Size.objects.all(),
        "selected_cats": set(selected_cats),
        "selected_colors": set(selected_colors),
        "selected_sizes": set(selected_sizes),
    }
    return render(request, "catalog/product_list.html", ctx)
