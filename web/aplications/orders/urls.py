from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
]
