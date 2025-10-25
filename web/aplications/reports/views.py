from datetime import datetime, timedelta
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Sum, F
from aplications.orders.models import Pedido, PedidoDetalle
from aplications.catalog.models import ProductoVariante
from .utils.pdf_report import generate_sales_pdf


@staff_member_required
def report_dashboard(request):
    # Rango de fechas
    start = request.GET.get('start')
    end = request.GET.get('end')

    if not start or not end:
        today = datetime.today()
        start_date = datetime(today.year, today.month, 1)
        end_date = today
    else:
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")

    # Ventas totales y ganancia estimada
    pedidos = Pedido.objects.filter(fecha__range=[start_date, end_date])
    ventas_total = pedidos.aggregate(total=Sum('total'))['total'] or 0
    ganancia_total = ventas_total * 0.15  # margen estimado

    cantidad_pedidos = pedidos.count()

    # Productos más vendidos
    detalles = PedidoDetalle.objects.filter(pedido__in=pedidos)
    top_products = (
        detalles.values('variante')
        .annotate(cantidad=Sum('cantidad'))
        .order_by('-cantidad')
    )

    productos_con_info = []
    for item in top_products:
        try:
            variante = ProductoVariante.objects.select_related('producto').get(pk=item['variante'])
            productos_con_info.append({'producto': variante.producto, 'cantidad': item['cantidad']})
        except ProductoVariante.DoesNotExist:
            pass

    paginator = Paginator(productos_con_info, 10)
    page_number = request.GET.get('page')
    top_products_page = paginator.get_page(page_number)

    # Ventas por semana
    weeks = []
    current = start_date
    while current < end_date:
        week_end = current + timedelta(days=6)
        week_sales = pedidos.filter(fecha__range=[current, week_end]).aggregate(total=Sum('total'))['total'] or 0
        weeks.append({'start': current.date(), 'end': week_end.date(), 'total': week_sales})
        current = week_end + timedelta(days=1)

    context = {
        'ventas_total': ventas_total,
        'ganancia_total': ganancia_total,
        'cantidad_pedidos': cantidad_pedidos,
        'top_products_page': top_products_page,
        'weeks': weeks,
        'start': start_date.date(),
        'end': end_date.date(),
    }

    return render(request, 'admin/reports_sales.html', context)


@staff_member_required
def export_pdf(request):
    start = request.GET.get('start')
    end = request.GET.get('end')

    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")

    pedidos = Pedido.objects.filter(fecha__range=[start_date, end_date])
    ventas_total = pedidos.aggregate(total=Sum('total'))['total'] or 0
    ganancia_total = ventas_total * 0.15
    cantidad_pedidos = pedidos.count()

    return generate_sales_pdf(ventas_total, cantidad_pedidos, ganancia_total)
