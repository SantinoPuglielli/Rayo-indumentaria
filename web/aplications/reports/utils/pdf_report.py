from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_sales_pdf(ventas_total, cantidad_pedidos, ganancia_total):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 18)
    p.drawString(200, 800, "Reporte de Ventas")

    p.setFont("Helvetica", 12)
    p.drawString(100, 750, f"Total de ventas: ${ventas_total:,.2f}")
    p.drawString(100, 730, f"Cantidad de pedidos: {cantidad_pedidos}")
    p.drawString(100, 710, f"Ganancia estimada: ${ganancia_total:,.2f}")

    p.showPage()
    p.save()

    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')
