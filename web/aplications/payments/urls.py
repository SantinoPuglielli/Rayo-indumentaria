from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    # Nueva ruta para pago por transferencia
    path("transferencia/", views.pago_transferencia, name="pago_transferencia"),
]
