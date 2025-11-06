from io import BytesIO
from decimal import Decimal
from datetime import datetime
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_sales_pdf(ventas_total, cantidad_pedidos, ganancia_total):
    # Convertir a Decimal si viene en otro tipo
    ventas_total = Decimal(str(ventas_total))
    ganancia_total = Decimal(str(ganancia_total))

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Título
    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(width / 2, height - 80, "📊 Reporte de Ventas")

    # Datos principales
    p.setFont("Helvetica", 12)
    p.drawString(100, height - 130, f"Total de ventas: ${ventas_total:,.2f}")
    p.drawString(100, height - 150, f"Cantidad de pedidos: {cantidad_pedidos}")
    p.drawString(100, height - 170, f"Ganancia estimada: ${ganancia_total:,.2f}")

    # Fecha de generación
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    p.setFont("Helvetica-Oblique", 10)
    p.drawRightString(width - 60, 50, f"Generado el {fecha}")

    # Finalizar PDF
    p.showPage()
    p.save()

    buffer.seek(0)

    # 🔹 Devolver como descarga
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_ventas.pdf"'
    return response
