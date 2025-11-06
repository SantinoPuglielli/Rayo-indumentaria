from datetime import datetime, timedelta
from decimal import Decimal
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponseBadRequest
from aplications.orders.models import Pedido, PedidoDetalle
from aplications.catalog.models import ProductoVariante
from .utils.pdf_report import generate_sales_pdf

@staff_member_required
def report_dashboard(request):
    start = request.GET.get('start')
    end = request.GET.get('end')

    # Si no hay fechas o están vacías, usar el mes actual
    if not start or not end or start.strip() == "" or end.strip() == "":
        today = datetime.today()
        start_date = datetime(today.year, today.month, 1)
        end_date = today + timedelta(days=1)
    else:
        try:
            start_date = datetime.strptime(start, "%Y-%m-%d")
            end_date = datetime.strptime(end, "%Y-%m-%d") + timedelta(days=1)
        except ValueError:
            # Si las fechas son inválidas, usar rango por defecto
            today = datetime.today()
            start_date = datetime(today.year, today.month, 1)
            end_date = today + timedelta(days=1)

    # 🔹 Consultar pedidos
    pedidos = Pedido.objects.filter(fecha__range=[start_date, end_date])
    ventas_total = pedidos.aggregate(total=Sum('total'))['total'] or Decimal('0')
    ganancia_total = ventas_total * Decimal('0.15')
    cantidad_pedidos = pedidos.count()

    # 🔹 Productos más vendidos
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
            productos_con_info.append({
                'producto': variante.producto,
                'cantidad': item['cantidad']
            })
        except ProductoVariante.DoesNotExist:
            pass

    paginator = Paginator(productos_con_info, 10)
    page_number = request.GET.get('page')
    top_products_page = paginator.get_page(page_number)

    # 🔹 Ventas por semana
    weeks = []
    current = start_date
    while current < end_date:
        week_end = current + timedelta(days=6)
        week_sales = pedidos.filter(fecha__range=[current, week_end]).aggregate(total=Sum('total'))['total'] or Decimal('0')
        weeks.append({
            'start': current.date(),
            'end': week_end.date(),
            'total': week_sales
        })
        current = week_end + timedelta(days=1)

    # 🔹 Contexto para template
    context = {
        'ventas_total': ventas_total,
        'ganancia_total': ganancia_total,
        'cantidad_pedidos': cantidad_pedidos,
        'top_products_page': top_products_page,
        'weeks': weeks,
        'start': start_date.date(),
        'end': (end_date - timedelta(days=1)).date(),  # corregimos visualmente el día final
    }

    return render(request, 'admin/reports_sales.html', context)


@staff_member_required
def export_pdf(request):
    from decimal import Decimal
    from datetime import datetime, timedelta
    from django.http import HttpResponseBadRequest

    start = request.GET.get('start')
    end = request.GET.get('end')

    # 🔹 Si no hay fechas o el formato es inválido, usar mes actual
    try:
        if not start or not end or start.strip() == "" or end.strip() == "":
            today = datetime.today()
            start_date = datetime(today.year, today.month, 1)
            end_date = today + timedelta(days=1)
        else:
            # intentar leer fechas ISO (YYYY-MM-DD)
            start_date = datetime.fromisoformat(start)
            end_date = datetime.fromisoformat(end) + timedelta(days=1)
    except Exception as e:
        print(f"[REPORTES] ❌ Error en fechas: {e}")
        today = datetime.today()
        start_date = datetime(today.year, today.month, 1)
        end_date = today + timedelta(days=1)

    # 🔹 Calcular totales
    pedidos = Pedido.objects.filter(fecha__range=[start_date, end_date])
    ventas_total = pedidos.aggregate(total=Sum('total'))['total'] or Decimal('0')
    ganancia_total = ventas_total * Decimal('0.15')
    cantidad_pedidos = pedidos.count()

    # 🔹 Exportar PDF
    return generate_sales_pdf(
        ventas_total=round(ventas_total, 2),
        cantidad_pedidos=cantidad_pedidos,
        ganancia_total=round(ganancia_total, 2),
    )
