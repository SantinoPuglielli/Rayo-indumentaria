from django.urls import path
from . import views

app_name = 'reports'  # 👈 esto es clave

urlpatterns = [
    path('', views.report_dashboard, name='dashboard'),
    path('export/pdf/', views.export_pdf, name='export_pdf'),
]
