from django.urls import path
from . import views

urlpatterns = [
    path('registros/', views.auditoria_list, name='auditoria_list'),
]
