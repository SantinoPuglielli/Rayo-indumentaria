from django.urls import path
from . import views

urlpatterns = [
    path('', views.report_dashboard, name='reports-dashboard'),
    path('export/pdf/', views.export_pdf, name='reports-export-pdf'),
]
