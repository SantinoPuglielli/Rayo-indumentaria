from django.contrib import admin
from django.urls import path
from django.db.models import Sum
from django.utils.timezone import now
from django.http import HttpResponse
import csv
from aplications.orders.models import Order

class ReportsAdminSite(admin.AdminSite):
    site_header = 'Rayo Indumentaria - Panel'
    site_title = 'Rayo Admin'

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path('reports/', self.admin_view(self.report_dashboard), name='reports'),
            path('reports/export.csv', self.admin_view(self.report_export_csv), name='report_export_csv'),
        ]
        return custom + urls

    def report_dashboard(self, request):
        from django.shortcuts import render
        today = now().date()
        qs = Order.objects.all()
        kpi_total = qs.aggregate(total=Sum('total_amount'))['total'] or 0
        kpi_aprobadas = qs.filter(status='approved').count()
        kpi_pendientes = qs.filter(status='pending').count()

        from datetime import timedelta
        labels, data = [], []
        for i in range(29,-1,-1):
            d = today - timedelta(days=i)
            day_total = qs.filter(created_at__date=d, status='approved').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
            labels.append(d.strftime('%d/%m'))
            data.append(float(day_total))
        ctx = {'kpi_total':kpi_total,'kpi_aprobadas':kpi_aprobadas,'kpi_pendientes':kpi_pendientes,
               'labels': labels, 'data': data}
        return render(request, 'admin/reports_dashboard.html', ctx)

    def report_export_csv(self, request):
        resp = HttpResponse(content_type='text/csv')
        resp['Content-Disposition'] = 'attachment; filename="ventas.csv"'
        writer = csv.writer(resp)
        writer.writerow(['ID','Estado','Total','Creado'])
        for o in Order.objects.all().values_list('id','status','total_amount','created_at'):
            writer.writerow(o)
        return resp

admin_site = ReportsAdminSite(name='reports_admin')
